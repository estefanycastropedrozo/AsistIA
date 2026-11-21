import os
import datetime
from typing import Optional
import jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "teinco_asistia_secret_key_2026_super_secure")
ALGORITHM = "HS256"

# Credenciales de administrador por defecto para demostración institucional
ADMIN_USER = {
    "email": "admin@teinco.edu.co",
    "password": "Teinco2026*",
    "name": "Coordinación de Tecnologías TEINCO",
    "role": "SuperAdmin"
}

security = HTTPBearer(auto_error=False)

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(hours=12))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> dict:
    if not credentials:
        raise HTTPException(status_code=401, detail="Se requiere inicio de sesión administrativo")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="La sesión ha expirado, ingresa nuevamente")
    except Exception:
        raise HTTPException(status_code=401, detail="Credenciales de acceso inválidas")

def verify_superadmin(payload: dict = Depends(verify_token)) -> dict:
    if payload.get("role") != "SuperAdmin":
        raise HTTPException(
            status_code=403,
            detail="Permiso denegado: Esta acción requiere privilegios de Super Administrador (Rectoría / Dirección General)."
        )
    return payload

