import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_token: Optional[str] = None
    message: str = Field(..., min_length=1, description="Consulta del usuario a AsistIA")
    user_role: Optional[str] = Field(default="estudiante", description="aspirante, estudiante, egresado, docente")

class DivisionContactInfo(BaseModel):
    division_name: str
    email: str
    phone: str
    office: str
    schedule: str

class ChatResponse(BaseModel):
    message_id: int
    session_token: str
    reply: str
    detected_division: str
    confidence_score: float
    response_time_ms: float
    sources: List[str]
    division_contact: Optional[DivisionContactInfo] = None

class FeedbackRequest(BaseModel):
    message_id: int
    is_helpful: bool
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    success: bool
    message: str

class KnowledgeArticleBase(BaseModel):
    division: str
    category: str
    title: str
    content: str
    keywords: Optional[str] = ""
    contact_email: Optional[str] = ""
    contact_phone: Optional[str] = ""
    office_location: Optional[str] = ""
    schedule: Optional[str] = ""

class KnowledgeArticleCreate(KnowledgeArticleBase):
    pass

class KnowledgeArticleRead(KnowledgeArticleBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

class QueryAuditItem(BaseModel):
    id: int
    session_token: str
    user_role: str
    user_query: str
    ai_reply: str
    detected_division: str
    confidence_score: float
    response_time_ms: float
    is_helpful: Optional[bool] = None
    created_at: datetime.datetime

class AnalyticsOverview(BaseModel):
    total_queries: int
    total_sessions: int
    positive_feedback: int
    negative_feedback: int
    satisfaction_rate: float
    avg_response_time_ms: float
    queries_by_division: Dict[str, int]
    queries_by_role: Dict[str, int]
    recent_interactions: List[QueryAuditItem]

class RuntimeSettingsUpdate(BaseModel):
    AI_PROVIDER: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: str
    user: Dict[str, Any]

class AdminUserCreate(BaseModel):
    email: str
    full_name: str
    password: str
    role: Optional[str] = "Operario"

class AdminUserRead(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True

