@echo off
title AsistIA - Backend TEINCO (FastAPI)
cd /d "%~dp0"
echo ========================================================
echo  Iniciando Backend AsistIA (FastAPI + RAG TEINCO)
echo  Servidor en: http://127.0.0.1:8000
echo  Documentacion API Swagger en: http://127.0.0.1:8000/docs
echo ========================================================
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
pause
