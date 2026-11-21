import os
import json
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
SETTINGS_FILE = BASE_DIR / "runtime_settings.json"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

class Settings:
    PROJECT_NAME: str = "AsistIA — TEINCO"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Asistente Conversacional con IA Generativa y RAG para divisiones de TEINCO"
    
    # Base de datos (SQLite por defecto para portabilidad inmediata, compatible con PostgreSQL)
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'asistia.db'}")
    
    # Motor de IA por defecto: "local_rag" (sin costo), "openai", o "gemini"
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "local_rag")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Orígenes permitidos en CORS
    CORS_ORIGINS: list = ["*"]
    
    def __init__(self):
        self.load_runtime_settings()
        
    def load_runtime_settings(self):
        """Carga ajustes modificados desde el panel administrativo en caliente."""
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "AI_PROVIDER" in data:
                        self.AI_PROVIDER = data["AI_PROVIDER"]
                    if "OPENAI_API_KEY" in data:
                        self.OPENAI_API_KEY = data["OPENAI_API_KEY"]
                    if "GEMINI_API_KEY" in data:
                        self.GEMINI_API_KEY = data["GEMINI_API_KEY"]
                    if "OPENAI_MODEL" in data:
                        self.OPENAI_MODEL = data["OPENAI_MODEL"]
                    if "GEMINI_MODEL" in data:
                        self.GEMINI_MODEL = data["GEMINI_MODEL"]
            except Exception as e:
                print(f"Error cargando runtime_settings: {e}")
                
    def save_runtime_settings(self, updates: dict):
        """Guarda ajustes desde el panel de control institucional."""
        current = {}
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    current = json.load(f)
            except Exception:
                current = {}
        current.update(updates)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
        self.load_runtime_settings()

settings = Settings()
