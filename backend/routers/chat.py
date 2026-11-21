import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ConversationSession, ChatMessage, MessageFeedback
from ..schemas import ChatRequest, ChatResponse, FeedbackRequest, FeedbackResponse, DivisionContactInfo
from ..rag_service import generate_rag_response, sanitize_pii
from ..knowledge_base import TEINCO_DIVISIONS_CONTACT

router = APIRouter(prefix="/api/chat", tags=["Chat AsistIA"])

@router.post("", response_model=ChatResponse)
async def process_chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Endpoint principal para interactuar con AsistIA.
    Procesa la consulta del estudiante mediante RAG, clasifica la división y persiste la interacción.
    """
    # 1. Resolver o crear sesión de usuario
    session_token = request.session_token
    if not session_token:
        session_token = str(uuid.uuid4())
        session = ConversationSession(session_token=session_token, user_role=request.user_role)
        db.add(session)
        db.commit()
        db.refresh(session)
    else:
        session = db.query(ConversationSession).filter_by(session_token=session_token).first()
        if not session:
            session = ConversationSession(session_token=session_token, user_role=request.user_role)
            db.add(session)
            db.commit()
            db.refresh(session)
        elif request.user_role and session.user_role != request.user_role:
            session.user_role = request.user_role
            db.commit()

    # 2. Sanitizar consulta del usuario para el registro (Ley 1581)
    sanitized_user_query = sanitize_pii(request.message)

    # 3. Guardar mensaje del usuario
    user_msg = ChatMessage(
        session_id=session.id,
        sender="user",
        content=sanitized_user_query
    )
    db.add(user_msg)
    db.commit()

    # 4. Ejecutar pipeline RAG
    rag_result = await generate_rag_response(sanitized_user_query, user_role=session.user_role)

    # 5. Guardar respuesta del asistente con metadatos analíticos
    contact_obj = rag_result.get("division_contact")
    assistant_msg = ChatMessage(
        session_id=session.id,
        sender="assistant",
        content=rag_result["reply"],
        detected_division=rag_result["detected_division"],
        confidence_score=rag_result["confidence_score"],
        response_time_ms=rag_result["response_time_ms"],
        sources_cited=", ".join(rag_result["sources"])
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    division_contact_schema = None
    if contact_obj:
        division_contact_schema = DivisionContactInfo(**contact_obj)

    return ChatResponse(
        message_id=assistant_msg.id,
        session_token=session.session_token,
        reply=rag_result["reply"],
        detected_division=rag_result["detected_division"],
        confidence_score=rag_result["confidence_score"],
        response_time_ms=rag_result["response_time_ms"],
        sources=rag_result["sources"],
        division_contact=division_contact_schema
    )

@router.get("/history/{session_token}")
def get_chat_history(session_token: str, db: Session = Depends(get_db)):
    """Recupera el historial de conversación para una sesión activa."""
    session = db.query(ConversationSession).filter_by(session_token=session_token).first()
    if not session:
        return {"session_token": session_token, "messages": []}

    messages = (
        db.query(ChatMessage)
        .filter_by(session_id=session.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    history = []
    for msg in messages:
        feedback_data = None
        if msg.feedback:
            feedback_data = {
                "is_helpful": msg.feedback.is_helpful,
                "comment": msg.feedback.comment
            }
        history.append({
            "id": msg.id,
            "sender": msg.sender,
            "content": msg.content,
            "detected_division": msg.detected_division,
            "confidence_score": msg.confidence_score,
            "response_time_ms": msg.response_time_ms,
            "sources": [s.strip() for s in msg.sources_cited.split(",") if s.strip()] if msg.sources_cited else [],
            "feedback": feedback_data,
            "created_at": msg.created_at.isoformat()
        })

    return {
        "session_token": session_token,
        "user_role": session.user_role,
        "messages": history
    }

@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(feedback_data: FeedbackRequest, db: Session = Depends(get_db)):
    """Registra la calificación de satisfacción del usuario sobre una respuesta."""
    msg = db.query(ChatMessage).filter_by(id=feedback_data.message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")

    existing_feedback = db.query(MessageFeedback).filter_by(message_id=msg.id).first()
    if existing_feedback:
        existing_feedback.is_helpful = feedback_data.is_helpful
        existing_feedback.comment = feedback_data.comment
    else:
        new_feedback = MessageFeedback(
            message_id=msg.id,
            is_helpful=feedback_data.is_helpful,
            comment=feedback_data.comment
        )
        db.add(new_feedback)

    db.commit()
    return FeedbackResponse(success=True, message="Gracias por tu retroalimentación sobre el servicio de TEINCO.")

@router.get("/divisions")
def list_divisions():
    """Retorna la lista oficial de divisiones institucionales con datos de contacto y sugerencias."""
    divisions_list = []
    sample_queries = {
        "Admisiones y Mercadeo": [
            "¿Cuáles son los programas académicos y carreras que ofrece TEINCO en sus 3 facultades?",
            "¿Cuáles son los requisitos de inscripción para estudiantes nuevos?",
            "¿Cómo solicito una homologación desde otra universidad o el SENA?"
        ],
        "Registro y Control": [
            "¿Cómo solicito un certificado de notas o de estudio?",
            "¿Cuáles son los requisitos y fechas para postularme a grado?",
            "¿Cómo inscribir materias en el portal académico?"
        ],
        "Bienestar Institucional": [
            "¿Cómo agendar una cita de orientación psicológica gratuita?",
            "¿Cuáles son los requisitos para la Beca de Excelencia?",
            "¿Qué selecciones deportivas y talleres culturales tienen?"
        ],
        "Cartera y Financiación": [
            "¿Cuáles son las opciones de financiación y crédito directo?",
            "¿Cómo pagar la matrícula a través del botón PSE o bancos?",
            "¿Cómo obtengo mi Paz y Salvo financiero?"
        ],
        "Coordinación Académica": [
            "¿Qué requisitos debo cumplir para iniciar mis prácticas profesionales?",
            "¿Cuáles son las opciones de grado para Desarrollo de Software?",
            "¿Cuál es el trámite para un examen supletorio o habilitación?"
        ],
        "Soporte y Sistemas": [
            "Olvidé la contraseña de mi correo institucional o campus Moodle",
            "¿Cómo acceder a las aulas virtuales de TEINCO?"
        ]
    }
    for name, info in TEINCO_DIVISIONS_CONTACT.items():
        divisions_list.append({
            **info,
            "sample_queries": sample_queries.get(name, [])
        })
    return divisions_list
