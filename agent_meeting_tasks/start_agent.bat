@echo off
title Meeting-to-Tasks Agent Server
cd /d "%~dp0"
echo ===================================================
echo 🤖 Meeting-to-Tasks Agent (Ziro Hackathon 2026)
echo ===================================================
echo Starting FastAPI Web Dashboard on http://127.0.0.1:8050 ...
echo.
python server.py
pause
