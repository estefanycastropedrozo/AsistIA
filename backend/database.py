import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings, BASE_DIR

db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

connect_args = {}
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {"connect_timeout": 5}

try:
    engine = create_engine(
        db_url,
        connect_args=connect_args,
        pool_pre_ping=True,
        echo=False
    )
    # Verificacion inicial de conectividad
    if not db_url.startswith("sqlite"):
        with engine.connect() as test_conn:
            print("[DATABASE] Conexion exitosa a base de datos PostgreSQL/Supabase.")
except Exception as e:
    print(f"[DATABASE WARNING] No se pudo conectar a PostgreSQL ({e}). Activando SQLite local de contingencia.")
    local_sqlite = f"sqlite:///{BASE_DIR / 'asistia.db'}"
    engine = create_engine(
        local_sqlite,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

