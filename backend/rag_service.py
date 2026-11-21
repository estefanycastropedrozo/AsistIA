import re
import math
import time
import json
from typing import List, Dict, Tuple, Optional
import httpx
from .config import settings
from .knowledge_base import TEINCO_DIVISIONS_CONTACT, SEED_KNOWLEDGE_ARTICLES

# --- Sanitización de Datos Personales (Ley 1581 de 2012) ---
def sanitize_pii(text: str) -> str:
    """
    Anonimiza información personal identificable (cédulas colombianas, teléfonos, correos personales)
    para dar cumplimiento estricto a la Ley 1581 de 2012 y evitar fuga de datos personales.
    """
    text = re.sub(r'\b\d{7,10}\b', '[DOCUMENTO_PROTEGIDO]', text)
    text = re.sub(r'\b3\d{2}[-\s]?\d{3}[-\s]?\d{4}\b', '[CELULAR_PROTEGIDO]', text)
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@(?!teinco\.edu\.co)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[CORREO_PROTEGIDO]', text)
    return text

# --- Motor de Recuperación Semántica Vectorial (TF-IDF / Coseno) ---
class VectorRAGIndex:
    def __init__(self):
        self.documents: List[Dict] = []
        self.vocabulary: Dict[str, int] = {}
        self.doc_vectors: List[List[float]] = []
        self.idf: Dict[str, float] = {}
        self.rebuild_index(SEED_KNOWLEDGE_ARTICLES)

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        accents = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'ñ': 'n'}
        for orig, norm in accents.items():
            text = text.replace(orig, norm)
        tokens = re.findall(r'\b\w{3,}\b', text)
        stopwords = {
            'que', 'los', 'las', 'por', 'con', 'para', 'una', 'uno', 'unos', 'unas',
            'del', 'sobre', 'este', 'esta', 'estos', 'estas', 'como', 'donde', 'cuando',
            'cual', 'cuales', 'quien', 'quienes', 'pero', 'mas', 'porque', 'desde',
            'hasta', 'entre', 'hacia', 'sin', 'tras', 'teinco', 'institucion'
        }
        return [t for t in tokens if t not in stopwords]

    def rebuild_index(self, articles: List[Dict]):
        self.documents = articles
        num_docs = len(articles)
        if num_docs == 0:
            return

        doc_term_freqs = []
        doc_freq = {}

        for doc in articles:
            full_text = f"{doc.get('title', '')} {doc.get('category', '')} {doc.get('division', '')} {doc.get('keywords', '')} {doc.get('content', '')}"
            tokens = self._tokenize(full_text)
            term_counts = {}
            for token in tokens:
                term_counts[token] = term_counts.get(token, 0) + 1
            doc_term_freqs.append(term_counts)

            for term in set(tokens):
                doc_freq[term] = doc_freq.get(term, 0) + 1

        self.vocabulary = {term: idx for idx, term in enumerate(doc_freq.keys())}
        self.idf = {term: math.log((num_docs + 1) / (df + 1)) + 1.0 for term, df in doc_freq.items()}

        self.doc_vectors = []
        for tf in doc_term_freqs:
            vec = [0.0] * len(self.vocabulary)
            norm_sq = 0.0
            for term, count in tf.items():
                if term in self.vocabulary:
                    val = (1.0 + math.log(count)) * self.idf[term]
                    idx = self.vocabulary[term]
                    vec[idx] = val
                    norm_sq += val * val
            norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
            self.doc_vectors.append([v / norm for v in vec])

    def search(self, query: str, top_k: int = 4) -> List[Tuple[Dict, float]]:
        tokens = self._tokenize(query)
        if not tokens or not self.doc_vectors:
            return [(self.documents[0], 0.5)] if self.documents else []

        q_tf = {}
        for t in tokens:
            q_tf[t] = q_tf.get(t, 0) + 1

        q_vec = [0.0] * len(self.vocabulary)
        q_norm_sq = 0.0
        for term, count in q_tf.items():
            if term in self.vocabulary:
                val = (1.0 + math.log(count)) * self.idf[term]
                idx = self.vocabulary[term]
                q_vec[idx] = val
                q_norm_sq += val * val

        q_norm = math.sqrt(q_norm_sq) if q_norm_sq > 0 else 1.0
        q_vec_norm = [v / q_norm for v in q_vec]

        scores = []
        for i, d_vec in enumerate(self.doc_vectors):
            dot_product = sum(q_vec_norm[idx] * d_vec[idx] for idx in range(len(self.vocabulary)) if q_vec_norm[idx] > 0)
            scores.append((self.documents[i], dot_product))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

rag_index = VectorRAGIndex()

# --- Detección de Intenciones Conversacionales ---
def check_conversational_intent(query: str, user_role: str) -> Optional[Tuple[str, str]]:
    """
    Identifica si la entrada del usuario es un saludo, agradecimiento o despedida,
    evitando disparar artículos reglamentarios aleatorios.
    Retorna (respuesta, division_detectada) o None si es una consulta de trámite.
    """
    q = query.lower().strip()
    q_clean = re.sub(r'[^\w\s]', '', q)

    # 1. Saludos
    greetings = ["hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "que tal", "hola buenas", "saludos", "hola asistia", "oye"]
    if q_clean in greetings or any(q_clean.startswith(g + " ") for g in greetings):
        role_label = {
            "aspirante": "Aspirante a TEINCO",
            "estudiante": "Estudiante de TEINCO",
            "egresado": "Estimado/a Egresado/a",
            "docente": "Estimado/a Docente"
        }.get(user_role.lower(), "amigo/a de la comunidad TEINCO")

        reply = (
            f"¡Hola! Te doy la bienvenida a **AsistIA**, el asistente virtual oficial de **TEINCO**.\n\n"
            f"Como {role_label}, estoy aquí para orientarte en tus consultas institucionales. Puedo ayudarte con:\n\n"
            f"• 📋 **Admisiones:** Requisitos de ingreso, costos, homologaciones y oferta académica.\n"
            f"• 🎓 **Registro y Control:** Certificados de estudio y notas, matrículas y requisitos de grado.\n"
            f"• 💳 **Cartera:** Medios de pago (PSE, bancos), crédito directo e ICETEX.\n"
            f"• 🧠 **Bienestar:** Acompañamiento psicológico gratuito, deportes, cultura y becas.\n"
            f"• 💻 **Coordinación de Software:** Prácticas profesionales (70% créditos) y opciones de grado.\n\n"
            f"¿Qué trámite o consulta deseas realizar hoy?"
        )
        return reply, "General"

    # 2. Agradecimientos
    thanks = ["gracias", "muchas gracias", "te agradezco", "vale gracias", "mil gracias", "gracias por la ayuda", "listo gracias", "perfecto gracias"]
    if any(q_clean == t or q_clean.startswith(t) for t in thanks):
        reply = (
            "¡Con mucho gusto! En **TEINCO** estamos para apoyarte en tu formación y trayectoria académica.\n\n"
            "Si tienes cualquier otra inquietud sobre certificados, pagos, materias o bienestar, aquí estaré para orientarte."
        )
        return reply, "General"

    # 3. Despedidas
    byes = ["chao", "adios", "hasta luego", "nos vemos", "chao gracias", "buen dia"]
    if any(q_clean == b for b in byes):
        reply = "¡Hasta luego! Que tengas un excelente día en tus actividades. Recuerda que **AsistIA** está disponible 24/7 para ti."
        return reply, "General"

    # 4. Preguntas de identidad / funciones
    identity_triggers = ["quien eres", "que eres", "que haces", "como funcionas", "para que sirves", "que puedes hacer"]
    if any(trigger in q_clean for trigger in identity_triggers):
        reply = (
            "Soy **AsistIA**, el asistente virtual inteligente de la **Corporación Tecnológica Industrial Colombiana (TEINCO)**.\n\n"
            "Fui desarrollado como proyecto de prácticas de la carrera de **Tecnología en Desarrollo de Software** para brindarte respuestas automáticas, oficiales y precisas sobre reglamentos, certificados, matrículas, pagos y bienestar.\n\n"
            "*(Tus consultas se tratan de forma confidencial y anónima bajo la Ley Estatutaria 1581 de 2012).* ¿En qué te puedo colaborar?"
        )
        return reply, "General"

    return None

def normalize_text(text: str) -> str:
    text = text.lower()
    accents = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'ñ': 'n'}
    for orig, norm in accents.items():
        text = text.replace(orig, norm)
    return text

def check_out_of_scope(query: str) -> Optional[str]:
    """
    Detecta de forma inteligente preguntas irrelevantes, fuera de contexto o ajenas a TEINCO
    (videojuegos como GTA, farándula, chistes, deportes externos, etc.) para responder con cortesía institucional.
    """
    q_norm = normalize_text(query)
    q_words = set(re.findall(r'\b\w+\b', q_norm))

    out_of_scope_keywords = [
        # Videojuegos y consolas
        "gta", "gtaiv", "gta4", "gtav", "gta5", "gtavi", "gta6", "grand theft auto",
        "playstation", "xbox", "nintendo", "fortnite", "minecraft", "fifa", "freefire",
        "roblox", "call of duty", "warzone", "gamer", "videojuego", "videojuegos",
        "play 5", "ps5", "ps4",
        # Entretenimiento ajeno, cine, chistes
        "chiste", "chistes", "cuentame un chiste", "dime un chiste", "meme", "memes",
        "pelicula", "peliculas", "serie", "series", "netflix", "marvel", "anime",
        "dragon ball", "goku", "naruto", "shakira", "bad bunny", "karol g", "cancion",
        # Deportes externos / celebridades
        "messi", "cristiano ronaldo", "real madrid", "barcelona fc", "champions league", "mundial de futbol",
        # Recetas / cosas domésticas
        "receta", "hamburguesa", "pizza", "como cocinar", "clima de manana", "horoscopo", "signo zodiacal",
        # Preguntas existenciales u off-topic
        "sentido de la vida", "eres real", "tienes sentimientos", "te quieres casar", "cuantos anos tienes"
    ]

    is_offtopic = any(k in q_norm for k in out_of_scope_keywords)

    # Detección de insultos / vulgaridades
    profanities = ["estupido", "tonto", "idiota", "bobo", "puta", "mierda", "gonorrea", "hp", "marica", "imbecil"]
    is_profane = any(p in q_words for p in profanities)

    if is_offtopic or is_profane:
        return (
            "Como asistente virtual oficial de la **Corporación Tecnológica Industrial Colombiana (TEINCO)**, "
            "mi función es orientarte exclusivamente en temas institucionales, académicos y administrativos.\n\n"
            "📌 **Temas en los que con gusto te puedo orientar:**\n"
            "1. **Admisiones:** Carreras de las 3 facultades, ciclos propedéuticos y requisitos de matrícula.\n"
            "2. **Registro y Control:** Certificados de notas y estudio, postulación a grado y calendarios.\n"
            "3. **Cartera y Financiación:** Medios de pago (PSE, bancos), crédito directo e ICETEX.\n"
            "4. **Bienestar Universitario:** Citas de psicología gratuitas, talleres culturales y becas de excelencia.\n"
            "5. **Coordinación y Soporte:** Opciones de grado (proyectos, diplomados), prácticas del 70% y campus virtual.\n\n"
            "No cuento con información sobre temas externos, videojuegos o entretenimiento no vinculados a **TEINCO**.\n\n"
            "¿En qué trámite o consulta sobre tu formación en la universidad te puedo colaborar?"
        )

    return None


# --- Clasificador de Dependencia Institucional ---
def detect_division(query: str, retrieved_articles: List[Tuple[Dict, float]]) -> Tuple[str, float]:
    q = normalize_text(query)

    # 1. Admisiones y Mercadeo (prioridad alta para inscripciones, programas, carreras, facultades)
    if any(k in q for k in [
        "inscrib", "inscripcion", "nuevo ingreso", "costo carrera", "que carreras",
        "oferta", "carrera", "carreras", "programa", "programas", "homologar", "sena",
        "facultad", "facultades", "mecatronica", "administracion", "contaduria", "diseno",
        "marketing", "mercadeo", "ciclos", "propedeutico", "estudiar"
    ]):
        return "Admisiones y Mercadeo", 0.98

    # 2. Registro y Control
    if any(k in q for k in ["certificado", "constancia", "notas", "sabana", "grado", "titulacion", "q10", "adicionar", "cancelar materia", "horario"]):
        return "Registro y Control", 0.98

    # 3. Bienestar Institucional
    if any(k in q for k in ["psicolog", "bienestar", "deporte", "futbol", "danza", "musica", "beca", "descuento", "enfermeria", "salud"]):
        return "Bienestar Institucional", 0.98

    # 4. Cartera y Financiación
    if any(k in q for k in ["pagar", "pago", "cuota", "cartera", "tesoreria", "pse", "banco", "icetex", "financia", "deuda", "paz y salvo"]):
        return "Cartera y Financiación", 0.98

    # 5. Coordinación Académica
    if any(k in q for k in ["practica", "pasantia", "malla", "pensum", "habilitacion", "supletorio", "opcion de grado", "modalidad de grado"]):
        return "Coordinación Académica", 0.98
    if "software" in q:
        return "Coordinación Académica", 0.90

    # 6. Soporte y Sistemas
    if any(k in q for k in ["correo institucional", "moodle", "clave", "contrasena", "contraseña", "acceso", "campus virtual", "bloqueo"]):
        return "Soporte y Sistemas", 0.98

    if retrieved_articles and retrieved_articles[0][1] > 0.15:
        top_doc, score = retrieved_articles[0]
        div = top_doc.get("division", "General")
        confidence = min(0.95, max(0.60, score * 1.5))
        return div, round(confidence, 2)

    return "General", 0.70

# --- Orquestador Principal RAG e Inferencia Generativa ---
async def generate_rag_response(query: str, user_role: str = "estudiante") -> Dict:
    start_time = time.time()
    sanitized_query = sanitize_pii(query)

    # 1. Comprobar intención conversacional primero (saludo, gracias, despedida)
    intent_result = check_conversational_intent(sanitized_query, user_role)
    if intent_result:
        reply_text, detected_div = intent_result
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "reply": reply_text,
            "detected_division": detected_div,
            "confidence_score": 1.0,
            "response_time_ms": elapsed_ms,
            "sources": ["Guion Conversacional AsistIA TEINCO"],
            "division_contact": None
        }

    # 1.1 Comprobar consultas fuera del ámbito institucional (videojuegos, farándula, chistes, etc.)
    out_of_scope_reply = check_out_of_scope(sanitized_query)
    if out_of_scope_reply:
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "reply": out_of_scope_reply,
            "detected_division": "Fuera de Contexto",
            "confidence_score": 1.0,
            "response_time_ms": elapsed_ms,
            "sources": ["Alcance Institucional Oficial TEINCO"],
            "division_contact": None
        }

    # 2. Recuperar coincidencias desde el índice vectorial
    raw_matches = rag_index.search(sanitized_query, top_k=6)

    # 2.1 Guardia semántica: si la similitud es nula y no contiene ninguna palabra institucional
    q_norm = normalize_text(sanitized_query)
    institutional_keywords = [
        "teinco", "carrera", "carreras", "semestre", "materia", "materias", "profesor", "docente",
        "estudiante", "grado", "grados", "titulo", "titulacion", "pago", "pagos", "matricula",
        "cuota", "certificado", "inscrip", "inscrib", "admision", "bienestar", "psicolog", "practica",
        "pasantia", "pensum", "credito", "cartera", "campus", "q10", "moodle", "facultad",
        "ingenieria", "sistemas", "software", "mecatronica", "administracion", "contaduria",
        "diseno", "marketing", "homolog", "sena", "diplomado", "supletorio", "habilitacion", "horario"
    ]
    has_institutional_kw = any(ik in q_norm for ik in institutional_keywords)
    max_raw_score = raw_matches[0][1] if raw_matches else 0.0

    if max_raw_score < 0.05 and not has_institutional_kw:
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "reply": (
                "Disculpa, no encontré en los reglamentos ni en la base institucional de **TEINCO** "
                "información relacionada con tu consulta.\n\n"
                "Como asistente virtual oficial, estoy orientada exclusivamente a resolver dudas sobre:\n\n"
                "• **Oferta Académica y Matrículas:** Programas de las 3 facultades y requisitos de ingreso.\n"
                "• **Trámites Estudiantiles:** Certificados de notas y estudio, y requisitos de grado.\n"
                "• **Cartera:** Pagos por PSE, bancos autorizados y opciones de financiación.\n"
                "• **Bienestar y Coordinación:** Citas de psicología, deportes, prácticas y opciones de grado.\n\n"
                "¿Podrías reformular tu consulta o indicarme sobre qué trámite de TEINCO deseas información?"
            ),
            "detected_division": "General",
            "confidence_score": 0.50,
            "response_time_ms": elapsed_ms,
            "sources": ["Guía Institucional TEINCO"],
            "division_contact": None
        }

    # 3. Detectar dependencia institucional
    division, confidence = detect_division(sanitized_query, raw_matches)
    division_contact = TEINCO_DIVISIONS_CONTACT.get(division, TEINCO_DIVISIONS_CONTACT.get("Registro y Control"))

    # 4. Re-ranking semántico favoreciendo la división detectada y palabras clave
    reranked = []
    for doc, base_score in raw_matches:
        score = base_score
        if doc.get("division") == division:
            score += 0.35
        title_lower = doc.get("title", "").lower()
        if any(w in q_norm for w in ["inscrib", "inscripcion", "nuevo"]) and "inscripcion" in title_lower:
            score += 0.40
        if any(w in q_norm for w in ["carrera", "carreras", "programa", "programas", "oferta", "facultad", "facultades"]) and any(k in title_lower for k in ["oferta", "carreras", "facultad", "programas"]):
            score += 0.45
        if any(w in q_norm for w in ["mecatronica", "automatizacion"]) and "mecatrónica" in title_lower:
            score += 0.50
        if any(w in q_norm for w in ["administracion", "contaduria", "contable", "tributaria"]) and "economicas" in title_lower:
            score += 0.50
        if any(w in q_norm for w in ["diseno", "marketing", "publicitari", "mercadeo"]) and "diseno" in title_lower:
            score += 0.50
        if any(w in q_norm for w in ["certificado", "constancia"]) and "certificado" in title_lower:
            score += 0.40
        if any(w in q_norm for w in ["opcion", "opciones", "modalidad", "modalidades"]) and "opciones" in title_lower:
            score += 0.55
        elif any(w in q_norm for w in ["grado", "titulacion"]) and "grado" in title_lower:
            score += 0.40
        if any(w in q_norm for w in ["pago", "cuota", "pagar", "pse"]) and any(p in title_lower for p in ["pago", "financiacion"]):
            score += 0.40
        if any(w in q_norm for w in ["practica", "pasantia"]) and "practica" in title_lower:
            score += 0.40
        if any(w in q_norm for w in ["psicolog", "estres"]) and "salud" in title_lower:
            score += 0.40
        reranked.append((doc, score))

    reranked.sort(key=lambda x: x[1], reverse=True)
    best_articles = [doc for doc, score in reranked[:3] if score > 0.15]
    if not best_articles and reranked:
        if max_raw_score > 0.04 or has_institutional_kw:
            best_articles = [reranked[0][0]]
        else:
            best_articles = []


    context_text = "\n\n".join([
        f"--- FUENTE INSTITUCIONAL: {a['title']} ({a['division']}) ---\n{a['content']}"
        for a in best_articles
    ])
    sources_cited = [a['title'] for a in best_articles]

    reply = ""

    # 5. Inferencia con Google Gemini si está configurado
    if settings.AI_PROVIDER == "gemini" and settings.GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
            prompt = (
                f"Eres AsistIA, el asistente virtual inteligente oficial de la Corporación Tecnológica Industrial Colombiana (TEINCO).\n"
                f"El usuario es: '{user_role}'.\n"
                f"Responde con tono institucional, profesional, empático y estructurado en Markdown.\n"
                f"Utiliza exclusivamente la siguiente normativa institucional de TEINCO:\n\n"
                f"{context_text}\n\n"
                f"Pregunta del usuario: {sanitized_query}\n"
                f"Instrucciones:\n"
                f"1. Da una respuesta directa, clara y con pasos numerados si aplica.\n"
                f"2. NO repitas al final la lista de correos o teléfonos, pues la interfaz gráfica ya muestra una tarjeta de contacto institucional debajo de tu mensaje.\n"
                f"3. Si la pregunta del usuario trata sobre temas externos, videojuegos (como GTA), entretenimiento ajeno o chistes, aclara cordialmente que AsistIA asesora exclusivamente temas institucionales de TEINCO.\n"
                f"4. Si la pregunta no se puede responder con la información dada, indícale amablemente al estudiante que contacte a {division}."
            )
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts:
                            reply = parts[0].get("text", "")
        except Exception as e:
            print(f"Fallback desde Gemini: {e}")

    # 6. Inferencia con OpenAI si está configurado
    elif settings.AI_PROVIDER == "openai" and settings.OPENAI_API_KEY:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
            messages = [
                {"role": "system", "content": (
                    f"Eres AsistIA, el asistente institucional de TEINCO. Atiendes a un usuario con rol '{user_role}'. "
                    f"Responde de forma clara, directa, amable y formateada en Markdown basándote en:\n{context_text}\n"
                    f"NO repitas al final datos de correo o teléfono en el texto, ya que la interfaz los muestra en una tarjeta visual."
                )},
                {"role": "user", "content": sanitized_query}
            ]
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, headers=headers, json={
                    "model": settings.OPENAI_MODEL,
                    "messages": messages,
                    "temperature": 0.3
                })
                if res.status_code == 200:
                    data = res.json()
                    reply = data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Fallback desde OpenAI: {e}")

    # 7. Motor RAG Semántico Local Directo (Sin duplicados y con respuestas claras)
    if not reply:
        reply = format_smart_local_rag(sanitized_query, user_role, division, best_articles)

    elapsed_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "reply": reply,
        "detected_division": division,
        "confidence_score": confidence,
        "response_time_ms": elapsed_ms,
        "sources": sources_cited,
        "division_contact": division_contact
    }

def split_steps_into_markdown(text: str) -> str:
    """
    Convierte textos con pasos consecutivos como '1) ... 2) ...' o '1. ... 2. ...'
    en listas numeradas escalonadas con saltos de línea independientes.
    Evita romper números decimales como 3.5 o 4.0.
    """
    import re
    if re.search(r'(1[\)\.]\s+.*?2[\)\.])', text):
        # Insertar salto antes del paso 1
        text = re.sub(r'(\s*:\s*|\.\s+)(1[\)\.])\s*', r':\n\n1. ', text)
        # Separar pasos subsiguientes (2, 3, 4...) en nuevas líneas evitando decimales como 3.5
        text = re.sub(r'(\s+)(\d+)\)\s*', r'\n\2. ', text)
        text = re.sub(r'(\s+)(\d+)\.(?!\d)\s*', r'\n\2. ', text)
    return text

def format_smart_local_rag(query: str, user_role: str, division: str, articles: List[Dict]) -> str:
    """
    Genera una respuesta contextual, estructurada y sin repeticiones de la tarjeta de contacto.
    """
    if not articles:
        return (
            "No encontré información reglamentaria en **TEINCO** directamente relacionada con tu consulta.\n\n"
            "Como asistente virtual oficial, puedo orientarte sobre:\n"
            "• **Admisiones:** Carreras de las 3 facultades, ciclos propedéuticos y requisitos de inscripción.\n"
            "• **Registro y Control:** Certificados de notas y estudio, postulación a grado y calendarios.\n"
            "• **Cartera:** Medios de pago (PSE, bancos), crédito directo e ICETEX.\n"
            "• **Bienestar y Coordinación:** Psicología gratuita, deportes, opciones de grado y campus virtual.\n\n"
            "Si se trata de un caso particular, te recomiendo consultar directamente con los canales oficiales en la tarjeta inferior."
        )

    primary = articles[0]
    additional = articles[1:] if len(articles) > 1 else []

    primary_content = split_steps_into_markdown(primary['content'])

    parts = [
        f"Respecto a tu consulta sobre **{primary['title']}**, esta es la directriz oficial de **TEINCO**:\n",
        f"{primary_content}\n"
    ]

    if additional:
        parts.append("\n📌 **Información complementaria:**")
        for extra in additional:
            extra_content = split_steps_into_markdown(extra['content'])
            parts.append(f"• **{extra['title']}:** {extra_content}")

    parts.append(
        f"\n💡 *En la tarjeta inferior encuentras los canales oficiales, horarios y sede de atención de {division}.* "
        f"¿Esta respuesta resolvió tu inquietud?"
    )

    return "\n".join(parts)
