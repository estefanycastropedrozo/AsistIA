import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import engine, Base
from .seed_data import seed_database
from .routers import chat, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar tablas y datos institucionales de TEINCO al iniciar
    seed_database()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan
)

# Configuración de CORS para permitir solicitudes desde el frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir enrutadores
app.include_router(chat.router)
app.include_router(admin.router)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "ai_provider": settings.AI_PROVIDER,
        "version": settings.VERSION
    }

# Servir frontend compilado en producción si existe la carpeta dist
DIST_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {
            "status": "online",
            "app": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "institution": "Corporación Tecnológica Industrial Colombiana (TEINCO)",
            "docs_url": "/docs"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
