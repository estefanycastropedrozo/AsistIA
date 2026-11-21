import uuid
import datetime
from .database import SessionLocal, Base, engine
from .models import KnowledgeArticle, ConversationSession, ChatMessage, MessageFeedback, AdminUser
from .knowledge_base import SEED_KNOWLEDGE_ARTICLES
from .rag_service import rag_index

def seed_database():
    """Inicializa la base de datos con reglamentos de TEINCO y datos de prueba institucionales."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"[WARN] Error en create_all: {e}")

    try:
        db = SessionLocal()
    except Exception as e:
        print(f"[WARN] Error abriendo sesion de BD: {e}")
        return

    try:
        # 1. Poblar artículos institucionales
        existing_count = db.query(KnowledgeArticle).count()
        if existing_count == 0:
            print("Cargando base de conocimiento oficial de TEINCO...")
            for item in SEED_KNOWLEDGE_ARTICLES:
                art = KnowledgeArticle(
                    division=item["division"],
                    category=item["category"],
                    title=item["title"],
                    content=item["content"],
                    keywords=item.get("keywords", ""),
                    contact_email=item.get("contact_email", ""),
                    contact_phone=item.get("contact_phone", ""),
                    office_location=item.get("office_location", ""),
                    schedule=item.get("schedule", "")
                )
                db.add(art)
            db.commit()
            print(f"Se cargaron {len(SEED_KNOWLEDGE_ARTICLES)} artículos institucionales.")

        # Reconstruir índice RAG a partir de la BD
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

        # 2. Poblar interacciones de demostración para el panel de analítica si está vacío
        session_count = db.query(ConversationSession).count()
        if session_count == 0:
            print("Poblando interacciones iniciales de demostración para el panel institucional...")
            demo_cases = [
                {
                    "role": "aspirante",
                    "query": "¿Cuáles son los requisitos de inscripción para Desarrollo de Software y qué horarios tienen?",
                    "reply": "Para inscribirte requieres documento de identidad, diploma de bachiller, pruebas Saber 11 y formulario web. TEINCO ofrece jornadas diurna, nocturna y sabatina.",
                    "division": "Admisiones y Mercadeo",
                    "time_ms": 320.5,
                    "confidence": 0.98,
                    "feedback": True
                },
                {
                    "role": "estudiante",
                    "query": "¿Cómo solicito un certificado de notas para presentar en mi trabajo?",
                    "reply": "Debes cancelar los derechos del certificado mediante PSE y enviar el comprobante a registroycontrol@teinco.edu.co. El tiempo de entrega es de 3 a 5 días hábiles.",
                    "division": "Registro y Control",
                    "time_ms": 280.2,
                    "confidence": 0.99,
                    "feedback": True
                },
                {
                    "role": "estudiante",
                    "query": "¿Qué opciones tengo para pagar la matrícula a plazos y qué convenios manejan?",
                    "reply": "Puedes optar por Crédito Directo TEINCO (40% de cuota inicial y cuotas mensuales) o líneas ICETEX y entidades aliadas como Fincomercio y Sufi.",
                    "division": "Cartera y Financiación",
                    "time_ms": 310.8,
                    "confidence": 0.97,
                    "feedback": True
                },
                {
                    "role": "estudiante",
                    "query": "¿Puedo pedir cita con el psicólogo de la universidad? ¿Tiene algún costo?",
                    "reply": "La atención psicológica en Bienestar Institucional es 100% gratuita y confidencial para todos los estudiantes activos de TEINCO.",
                    "division": "Bienestar Institucional",
                    "time_ms": 260.4,
                    "confidence": 0.98,
                    "feedback": True
                },
                {
                    "role": "estudiante",
                    "query": "¿Cuántos créditos necesito haber aprobado para iniciar mi práctica empresarial en software?",
                    "reply": "Requieres haber cursado y aprobado como mínimo el 70% de créditos del plan de estudios y radicar tu solicitud ante la Coordinación Académica.",
                    "division": "Coordinación Académica",
                    "time_ms": 295.0,
                    "confidence": 0.98,
                    "feedback": True
                },
                {
                    "role": "estudiante",
                    "query": "No puedo ingresar al campus virtual Moodle ni a mi correo de TEINCO.",
                    "reply": "Escribe a soporte.sistemas@teinco.edu.co adjuntando tu número de cédula para restablecer tus credenciales de acceso al Campus Virtual.",
                    "division": "Soporte y Sistemas",
                    "time_ms": 250.0,
                    "confidence": 0.98,
                    "feedback": True
                }
            ]

            now = datetime.datetime.utcnow()
            for i, case in enumerate(demo_cases):
                token = str(uuid.uuid4())
                sess = ConversationSession(
                    session_token=token,
                    user_role=case["role"],
                    created_at=now - datetime.timedelta(hours=i * 3)
                )
                db.add(sess)
                db.commit()
                db.refresh(sess)

                u_msg = ChatMessage(
                    session_id=sess.id,
                    sender="user",
                    content=case["query"],
                    created_at=sess.created_at
                )
                db.add(u_msg)
                db.commit()

                a_msg = ChatMessage(
                    session_id=sess.id,
                    sender="assistant",
                    content=case["reply"],
                    detected_division=case["division"],
                    confidence_score=case["confidence"],
                    response_time_ms=case["time_ms"],
                    sources_cited="Reglamento Estudiantil TEINCO",
                    created_at=sess.created_at + datetime.timedelta(seconds=1)
                )
                db.add(a_msg)
                db.commit()
                db.refresh(a_msg)

                fb = MessageFeedback(
                    message_id=a_msg.id,
                    is_helpful=case["feedback"],
                    comment="Excelente respuesta clara",
                    created_at=a_msg.created_at + datetime.timedelta(seconds=5)
                )
                db.add(fb)

            db.commit()
            print("Datos de demostración institucionales cargados con éxito.")

        # 3. Poblar usuarios administrativos con control de roles (RBAC) si está vacío
        user_count = db.query(AdminUser).count()
        if user_count == 0:
            print("Inicializando usuarios administrativos y roles (Rectoría/SuperAdmin y Coordinación/Operario)...")
            super_admin = AdminUser(
                email="admin@teinco.edu.co",
                full_name="Rectoría y Dirección General TEINCO",
                password_hash="Teinco2026*",
                role="SuperAdmin",
                is_active=True
            )
            operario = AdminUser(
                email="coordinador@teinco.edu.co",
                full_name="Coordinación de Registro y Control",
                password_hash="Teinco2026*",
                role="Operario",
                is_active=True
            )
            db.add(super_admin)
            db.add(operario)
            db.commit()
            print("Usuarios administrativos inicializados exitosamente.")


    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
