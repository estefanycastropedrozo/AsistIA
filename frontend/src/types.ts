export interface DivisionContactInfo {
  division_name: string;
  email: string;
  phone: string;
  office: string;
  schedule: string;
  sample_queries?: string[];
}

export interface ChatMessageItem {
  id?: number;
  sender: 'user' | 'assistant';
  content: string;
  detected_division?: string;
  confidence_score?: number;
  response_time_ms?: number;
  sources?: string[];
  division_contact?: DivisionContactInfo;
  feedback?: {
    is_helpful: boolean;
    comment?: string;
  } | null;
  created_at?: string;
}

export interface QueryAuditItem {
  id: number;
  session_token: string;
  user_role: string;
  user_query: string;
  ai_reply: string;
  detected_division: string;
  confidence_score: number;
  response_time_ms: number;
  is_helpful: boolean | null;
  created_at: string;
}

export interface AnalyticsOverview {
  total_queries: number;
  total_sessions: number;
  positive_feedback: number;
  negative_feedback: number;
  satisfaction_rate: number;
  avg_response_time_ms: number;
  queries_by_division: Record<string, number>;
  queries_by_role: Record<string, number>;
  recent_interactions: QueryAuditItem[];
}

export interface KnowledgeArticle {
  id: number;
  division: string;
  category: string;
  title: string;
  content: string;
  keywords: string;
  contact_email: string;
  contact_phone: string;
  office_location: string;
  schedule: string;
  created_at: string;
  updated_at: string;
}

export interface RuntimeSettings {
  AI_PROVIDER: string;
  OPENAI_MODEL: string;
  OPENAI_API_KEY_MASKED: string;
  HAS_OPENAI_KEY: boolean;
  GEMINI_MODEL: string;
  GEMINI_API_KEY_MASKED: string;
  HAS_GEMINI_KEY: boolean;
}

export interface AdminUser {
  id: number;
  email: string;
  full_name: string;
  role: 'SuperAdmin' | 'Operario' | string;
  is_active: boolean;
  created_at: string;
}

