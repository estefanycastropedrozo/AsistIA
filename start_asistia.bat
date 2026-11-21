@echo off
title Lanzador de AsistIA - TEINCO
cd /d "%~dp0"
echo ======================================================================
echo    CORPORACION TECNOLOGICA INDUSTRIAL COLOMBIANA - TEINCO
echo    ASISTIA - ASISTENTE CONVERSACIONAL CON IA Y PANEL DE REPORTES
echo ======================================================================
echo.
echo 1. Iniciando servidor Backend (FastAPI en puerto 8000)...
start "AsistIA - Backend (FastAPI)" cmd /c "run_backend.bat"

echo 2. Esperando 2 segundos...
timeout /t 2 /nobreak >nul

echo 3. Iniciando servidor Frontend (React en puerto 3000)...
start "AsistIA - Frontend (React)" cmd /c "run_frontend.bat"

echo 4. Abriendo aplicativo institucional en tu navegador...
timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000

echo.
echo ======================================================================
echo  Plataforma AsistIA en ejecucion:
echo  - Aplicativo Web Principal: http://127.0.0.1:8000
echo  - Servidor de Desarrollo React: http://localhost:3000
echo  - Documentacion Swagger: http://127.0.0.1:8000/docs
echo ======================================================================
echo.
