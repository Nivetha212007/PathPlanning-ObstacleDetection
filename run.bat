@echo off
cd /d "%~dp0"
where py >nul 2>nul && set "PY=py" || set "PY=python"
if not exist ".venv\Scripts\python.exe" %PY% -m venv .venv
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
".venv\Scripts\python.exe" main.py
pause
