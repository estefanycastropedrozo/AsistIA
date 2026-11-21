import csv
import io
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import ConversationSession, ChatMessage, MessageFeedback, KnowledgeArticle, AdminUser
from ..schemas import (
    AnalyticsOverview, QueryAuditItem, KnowledgeArticleCreate,
    KnowledgeArticleRead, RuntimeSettingsUpdate, LoginRequest, LoginResponse,
    AdminUserCreate, AdminUserRead
)
from ..config import settings
from ..rag_service import rag_index
from ..auth import ADMIN_USER, create_access_token, verify_token, verify_superadmin
from ..pdf_service import process_pdf_and_index

router = APIRouter(prefix="/api/admin", tags=["Panel Administrativo TEINCO"])

@router.post("/login", response_model=LoginResponse)
def admin_login(creds: LoginRequest, db: Session = Depends(get_db)):
    """Autenticación para acceso seguro al panel administrativo de TEINCO (Rectoría, Coordinadores y Operarios)."""
    email_clean = creds.email.strip().lower()
    user = db.query(AdminUser).filter(func.lower(AdminUser.email) == email_clean).first()

    if user and user.is_active and user.password_hash == creds.password:
        token = create_access_token({
            "sub": user.email,
            "name": user.full_name,
            "role": user.role
        })
        return LoginResponse(
            success=True,
            token=token,
            user={"email": user.email, "name": user.full_name, "role": user.role}
        )

    # Fallback a ADMIN_USER predeterminado
    if email_clean == ADMIN_USER["email"] and creds.password == ADMIN_USER["password"]:
        token = create_access_token({
            "sub": ADMIN_USER["email"],
            "name": ADMIN_USER["name"],
            "role": ADMIN_USER["role"]
        })
        return LoginResponse(
            success=True,
            token=token,
            user={"email": ADMIN_USER["email"], "name": ADMIN_USER["name"], "role": ADMIN_USER["role"]}
        )

    raise HTTPException(status_code=401, detail="Correo o contraseña institucional incorrectos o usuario inactivo")

@router.get("/users", response_model=List[AdminUserRead])
def list_admin_users(super_admin: dict = Depends(verify_superadmin), db: Session = Depends(get_db)):
    """Lista todos los funcionarios y usuarios con acceso administrativo (Exclusivo Rectoría/SuperAdmin)."""
    return db.query(AdminUser).order_by(AdminUser.role.asc(), AdminUser.created_at.desc()).all()

@router.post("/users", response_model=AdminUserRead)
def create_admin_user(user_in: AdminUserCreate, super_admin: dict = Depends(verify_superadmin), db: Session = Depends(get_db)):
    """Permite al Super Administrador (Rectoría/Vicerrectoría) registrar un nuevo funcionario (Operario o Administrador)."""
    email_clean = user_in.email.strip().lower()
    existing = db.query(AdminUser).filter(func.lower(AdminUser.email) == email_clean).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un funcionario registrado con este correo institucional")

    new_user = AdminUser(
        email=email_clean,
        full_name=user_in.full_name.strip(),
        password_hash=user_in.password,
        role=user_in.role if user_in.role in ["SuperAdmin", "Operario"] else "Operario",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/users/{user_id}")
def delete_admin_user(user_id: int, super_admin: dict = Depends(verify_superadmin), db: Session = Depends(get_db)):
    """Permite al Super Administrador desvincular o eliminar a un funcionario que ya no trabaja en TEINCO."""
    target_user = db.query(AdminUser).filter_by(id=user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if target_user.email.lower() == super_admin.get("sub", "").lower():
        raise HTTPException(status_code=400, detail="No puedes eliminar tu propia cuenta de Super Administrador activa")

    db.delete(target_user)
    db.commit()
    return {"success": True, "message": f"Usuario {target_user.full_name} ({target_user.email}) eliminado exitosamente"}


@router.get("/verify")
def verify_admin_session(user: dict = Depends(verify_token)):
    """Verifica si el token administrativo sigue vigente."""
    return {"valid": True, "user": user}

@router.post("/upload-pdf")
async def upload_institutional_pdf(
    file: UploadFile = File(...),
    division: str = Form("Registro y Control"),
    db: Session = Depends(get_db)
):
    """Permite a los administradores subir reglamentos en PDF e indexarlos en caliente en el RAG."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos en formato PDF (.pdf)")

    content = await file.read()
    if len(content) > 15 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="El archivo excede el límite permitido de 15 MB")

    try:
        articles = process_pdf_and_index(content, file.filename, division, db)
        return {
            "success": True,
            "filename": file.filename,
            "division": division,
            "chunks_indexed": len(articles),
            "message": f"Se procesaron e indexaron exitosamente {len(articles)} secciones del documento en el motor RAG de TEINCO."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando documento PDF: {str(e)}")


@router.get("/metrics", response_model=AnalyticsOverview)
def get_analytics_metrics(db: Session = Depends(get_db)):
    """Calcula las métricas e indicadores de rendimiento institucional en tiempo real."""
    total_sessions = db.query(ConversationSession).count()
    
    # Mensajes enviados por usuarios (consultas reales)
    total_queries = db.query(ChatMessage).filter_by(sender="user").count()

    # Feedback de satisfacción
    positive_feedback = db.query(MessageFeedback).filter_by(is_helpful=True).count()
    negative_feedback = db.query(MessageFeedback).filter_by(is_helpful=False).count()
    total_feedback = positive_feedback + negative_feedback
    satisfaction_rate = round((positive_feedback / total_feedback * 100), 1) if total_feedback > 0 else 100.0

    # Tiempo de respuesta promedio (de respuestas del asistente)
    avg_time = (
        db.query(func.avg(ChatMessage.response_time_ms))
        .filter(ChatMessage.sender == "assistant", ChatMessage.response_time_ms > 0)
        .scalar()
    ) or 0.0

    # Consultas por división institucional
    division_rows = (
        db.query(ChatMessage.detected_division, func.count(ChatMessage.id))
        .filter(ChatMessage.sender == "assistant")
        .group_by(ChatMessage.detected_division)
        .all()
    )
    queries_by_division = {row[0]: row[1] for row in division_rows}

    # Consultas por rol de usuario
    role_rows = (
        db.query(ConversationSession.user_role, func.count(ChatMessage.id))
        .join(ChatMessage, ChatMessage.session_id == ConversationSession.id)
        .filter(ChatMessage.sender == "user")
        .group_by(ConversationSession.user_role)
        .all()
    )
    queries_by_role = {row[0]: row[1] for row in role_rows}

    # Interacciones recientes para la bitácora de auditoría
    # Emparejamos cada mensaje de usuario con la respuesta inmediata del asistente
    assistant_msgs = (
        db.query(ChatMessage)
        .filter_by(sender="assistant")
        .order_by(ChatMessage.created_at.desc())
        .limit(30)
        .all()
    )

    recent_interactions: List[QueryAuditItem] = []
    for a_msg in assistant_msgs:
        # Buscar el mensaje de usuario previo en la misma sesión
        u_msg = (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == a_msg.session_id, ChatMessage.sender == "user", ChatMessage.created_at <= a_msg.created_at)
            .order_by(ChatMessage.created_at.desc())
            .first()
        )
        user_query_text = u_msg.content if u_msg else "Consulta de sesión"
        session_obj = db.query(ConversationSession).filter_by(id=a_msg.session_id).first()
        role = session_obj.user_role if session_obj else "estudiante"
        token = session_obj.session_token if session_obj else "anon"

        feedback_val = None
        if a_msg.feedback:
            feedback_val = a_msg.feedback.is_helpful

        recent_interactions.append(QueryAuditItem(
            id=a_msg.id,
            session_token=token[:8] + "...",
            user_role=role,
            user_query=user_query_text,
            ai_reply=a_msg.content[:160] + "..." if len(a_msg.content) > 160 else a_msg.content,
            detected_division=a_msg.detected_division or "General",
            confidence_score=a_msg.confidence_score or 0.95,
            response_time_ms=a_msg.response_time_ms or 0.0,
            is_helpful=feedback_val,
            created_at=a_msg.created_at
        ))

    return AnalyticsOverview(
        total_queries=total_queries,
        total_sessions=total_sessions,
        positive_feedback=positive_feedback,
        negative_feedback=negative_feedback,
        satisfaction_rate=satisfaction_rate,
        avg_response_time_ms=round(avg_time, 2),
        queries_by_division=queries_by_division,
        queries_by_role=queries_by_role,
        recent_interactions=recent_interactions
    )

@router.get("/export-csv")
def export_queries_csv(db: Session = Depends(get_db)):
    """Exporta las consultas e interacciones institucionales en formato CSV para informes gerenciales."""
    assistant_msgs = (
        db.query(ChatMessage)
        .filter_by(sender="assistant")
        .order_by(ChatMessage.created_at.desc())
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Fecha_Hora", "Rol_Usuario", "Consulta_Estudiante", "Division_Detectada",
        "Tiempo_Respuesta_MS", "Nivel_Confianza", "Satisfaccion_Usuario"
    ])

    for a_msg in assistant_msgs:
        u_msg = (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == a_msg.session_id, ChatMessage.sender == "user", ChatMessage.created_at <= a_msg.created_at)
            .order_by(ChatMessage.created_at.desc())
            .first()
        )
        session_obj = db.query(ConversationSession).filter_by(id=a_msg.session_id).first()
        role = session_obj.user_role if session_obj else "estudiante"
        user_text = u_msg.content if u_msg else ""
        satisfaction = "Sin calificar"
        if a_msg.feedback:
            satisfaction = "Útil" if a_msg.feedback.is_helpful else "No útil"

        writer.writerow([
            a_msg.id,
            a_msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            role,
            user_text,
            a_msg.detected_division,
            a_msg.response_time_ms,
            f"{int(a_msg.confidence_score * 100)}%",
            satisfaction
        ])

    csv_data = output.getvalue()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=informe_asistia_teinco.csv"}
    )

@router.post("/clear-history")
def clear_interaction_history(token_payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Limpia el historial de interacciones de prueba de la base de datos."""
    db.query(MessageFeedback).delete()
    db.query(ChatMessage).delete()
    db.query(ConversationSession).delete()
    db.commit()
    return {"success": True, "message": "Historial de pruebas limpiado correctamente."}

@router.get("/knowledge-base", response_model=List[KnowledgeArticleRead])
def list_knowledge_articles(db: Session = Depends(get_db)):
    """Lista todos los artículos y reglamentos almacenados en la base de conocimiento."""
    return db.query(KnowledgeArticle).order_by(KnowledgeArticle.division.asc(), KnowledgeArticle.title.asc()).all()

@router.post("/knowledge-base", response_model=KnowledgeArticleRead)
def create_knowledge_article(article_in: KnowledgeArticleCreate, db: Session = Depends(get_db)):
    """Permite a los administradores registrar un nuevo documento o trámite institucional."""
    db_article = KnowledgeArticle(**article_in.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    # Actualizar índice RAG en caliente
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

    return db_article

@router.delete("/knowledge-base/{article_id}")
def delete_knowledge_article(article_id: int, db: Session = Depends(get_db)):
    """Elimina un artículo de la base de conocimiento."""
    article = db.query(KnowledgeArticle).filter_by(id=article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    db.delete(article)
    db.commit()

    # Reconstruir índice RAG
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

    return {"success": True, "message": "Artículo eliminado"}

@router.put("/knowledge-base/{article_id}", response_model=KnowledgeArticleRead)
def update_knowledge_article(
    article_id: int,
    article_in: KnowledgeArticleCreate,
    token_payload: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Permite a los administradores editar un artículo existente en la base de conocimiento."""
    article = db.query(KnowledgeArticle).filter_by(id=article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    article.division = article_in.division
    article.category = article_in.category
    article.title = article_in.title
    article.content = article_in.content
    article.keywords = article_in.keywords
    article.contact_email = article_in.contact_email
    article.contact_phone = article_in.contact_phone
    article.office_location = article_in.office_location
    article.schedule = article_in.schedule

    db.commit()
    db.refresh(article)

    # Reconstruir índice RAG en caliente
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

    return article

@router.get("/settings")
def get_runtime_settings():
    """Consulta la configuración del motor de IA (enmascarando claves secretas)."""
    masked_openai = ""
    if settings.OPENAI_API_KEY:
        masked_openai = settings.OPENAI_API_KEY[:4] + "..." + settings.OPENAI_API_KEY[-4:]
    
    masked_gemini = ""
    if settings.GEMINI_API_KEY:
        masked_gemini = settings.GEMINI_API_KEY[:4] + "..." + settings.GEMINI_API_KEY[-4:]

    return {
        "AI_PROVIDER": settings.AI_PROVIDER,
        "OPENAI_MODEL": settings.OPENAI_MODEL,
        "OPENAI_API_KEY_MASKED": masked_openai,
        "HAS_OPENAI_KEY": bool(settings.OPENAI_API_KEY),
        "GEMINI_MODEL": settings.GEMINI_MODEL,
        "GEMINI_API_KEY_MASKED": masked_gemini,
        "HAS_GEMINI_KEY": bool(settings.GEMINI_API_KEY)
    }

@router.post("/settings")
def update_runtime_settings(updates: RuntimeSettingsUpdate):
    """Actualiza en tiempo de ejecución las claves y el modelo de IA desde el panel de control."""
    data = {}
    if updates.AI_PROVIDER is not None:
        data["AI_PROVIDER"] = updates.AI_PROVIDER
    if updates.OPENAI_API_KEY is not None and updates.OPENAI_API_KEY.strip():
        data["OPENAI_API_KEY"] = updates.OPENAI_API_KEY.strip()
    if updates.OPENAI_MODEL is not None:
        data["OPENAI_MODEL"] = updates.OPENAI_MODEL
    if updates.GEMINI_API_KEY is not None and updates.GEMINI_API_KEY.strip():
        data["GEMINI_API_KEY"] = updates.GEMINI_API_KEY.strip()
    if updates.GEMINI_MODEL is not None:
        data["GEMINI_MODEL"] = updates.GEMINI_MODEL

    settings.save_runtime_settings(data)
    return {"success": True, "message": "Configuración de IA actualizada correctamente"}
