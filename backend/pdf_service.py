import re
import io
from typing import List, Dict
import pypdf
from sqlalchemy.orm import Session
from .models import KnowledgeArticle
from .rag_service import rag_index
from .knowledge_base import TEINCO_DIVISIONS_CONTACT

def process_pdf_and_index(
    file_bytes: bytes,
    filename: str,
    division: str,
    db: Session
) -> List[KnowledgeArticle]:
    """
    Extrae texto de un archivo PDF institucional de TEINCO, lo divide en
    fragmentos semánticos, los persiste en la BD y reconstruye el índice RAG.
    """
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    full_text = ""
    for page_idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        full_text += f"\n[Página {page_idx + 1}]\n" + text

    # Limpiar espacios en blanco excesivos
    full_text = re.sub(r'[ \t]+', ' ', full_text)
    full_text = re.sub(r'\n{3,}', '\n\n', full_text).strip()

    if not full_text:
        return []

    # Dividir por secciones o párrafos de aproximadamente 600 - 900 caracteres
    raw_paragraphs = [p.strip() for p in full_text.split('\n\n') if len(p.strip()) > 40]
    
    chunks = []
    current_chunk = ""
    for p in raw_paragraphs:
        if len(current_chunk) + len(p) < 800:
            current_chunk += " " + p if current_chunk else p
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = p
    if current_chunk:
        chunks.append(current_chunk.strip())

    base_name = filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
    contact = TEINCO_DIVISIONS_CONTACT.get(division, TEINCO_DIVISIONS_CONTACT["Registro y Control"])

    created_articles = []
    for idx, chunk in enumerate(chunks[:15]): # Máximo 15 fragmentos por documento
        title = f"{base_name} — Parte {idx + 1}"
        # Extraer palabras clave básicas del fragmento
        keywords = ", ".join(list(set(re.findall(r'\b[a-záéíóúñ]{5,}\b', chunk.lower())))[:8])

        article = KnowledgeArticle(
            division=division,
            category=f"Documento PDF ({base_name})",
            title=title,
            content=chunk,
            keywords=keywords,
            contact_email=contact.get("email", ""),
            contact_phone=contact.get("phone", ""),
            office_location=contact.get("office", ""),
            schedule=contact.get("schedule", "")
        )
        db.add(article)
        created_articles.append(article)

    db.commit()

    # Reconstruir índice RAG en memoria con el nuevo documento
    all_articles = db.query(KnowledgeArticle).all()
    dicts = [
        {
            "id": a.id,
            "division": a.division,
            "category": a.category,
            "title": a.title,
            "content": a.content,
            "keywords": a.keywords
        }
        for a in all_articles
    ]
    rag_index.rebuild_index(dicts)

    return created_articles
