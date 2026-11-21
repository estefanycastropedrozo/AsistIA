import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class ConversationSession(Base):
    __tablename__ = "conversation_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String(64), unique=True, index=True, nullable=False)
    user_role = Column(String(50), default="estudiante") # aspirante, estudiante, egresado, docente
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_active = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("conversation_sessions.id"), nullable=False)
    sender = Column(String(20), nullable=False) # 'user' o 'assistant'
    content = Column(Text, nullable=False)
    
    # Metadatos analíticos y RAG
    detected_division = Column(String(100), default="General")
    confidence_score = Column(Float, default=0.95)
    response_time_ms = Column(Float, default=0.0)
    sources_cited = Column(Text, default="") # JSON o texto con fuentes de TEINCO citadas
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("ConversationSession", back_populates="messages")
    feedback = relationship("MessageFeedback", back_populates="message", uselist=False, cascade="all, delete-orphan")


class MessageFeedback(Base):
    __tablename__ = "message_feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("chat_messages.id"), nullable=False)
    is_helpful = Column(Boolean, nullable=False) # True = Pulgar arriba, False = Pulgar abajo
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    message = relationship("ChatMessage", back_populates="feedback")


class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"

    id = Column(Integer, primary_key=True, index=True)
    division = Column(String(100), index=True, nullable=False)
    category = Column(String(100), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    keywords = Column(Text, default="")
    
    # Información de contacto directo para la canalización institucional
    contact_email = Column(String(100), default="")
    contact_phone = Column(String(100), default="")
    office_location = Column(String(150), default="")
    schedule = Column(String(150), default="")
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="Operario")  # "SuperAdmin" o "Operario"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

