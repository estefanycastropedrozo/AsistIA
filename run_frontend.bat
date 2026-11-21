@echo off
title AsistIA - Frontend TEINCO (React + Vite)
cd /d "%~dp0frontend"
echo ========================================================
echo  Iniciando Frontend AsistIA (React + Vite)
echo  Abriendo en: http://localhost:3000
echo ========================================================
call npm.cmd run dev
pause
