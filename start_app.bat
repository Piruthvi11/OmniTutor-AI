@echo off
title OmniTutor AI Web Server - Team CODEFORGE
echo ========================================================
echo   Starting OmniTutor AI (Track D Multimodal Assistant)
echo   Team CODEFORGE - Bannari Amman Institute of Technology
echo ========================================================
echo.
echo Opening browser at http://localhost:8000 ...
start http://localhost:8000
echo.
python -m uvicorn server:app --host 0.0.0.0 --port 8000
pause
