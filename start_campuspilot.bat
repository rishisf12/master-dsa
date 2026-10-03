@echo off
REM CampusPilot Start Script (Batch version)
REM Runs backend with venv and frontend

set ROOT_DIR=%~dp0
set BACKEND_DIR=%ROOT_DIR%CampusPilot\backend\backend
set FRONTEND_DIR=%ROOT_DIR%CampusPilot\frontend
set VENV_DIR=%BACKEND_DIR%\.venv

REM Check for Python 3.10, 3.11, or 3.12
set PYTHON_CMD=
for %%v in (3.12 3.11 3.10) do (
    if not defined PYTHON_CMD (
        py -%%v -c "import sys" 2>nul && set PYTHON_CMD=py -%%v
    )
)
if not defined PYTHON_CMD (
    echo ERROR: Python 3.10, 3.11, or 3.12 required. Please install one of these versions.
    echo Use "py -3.10", "py -3.11", or "py -3.12" to verify.
    pause
    exit /b 1
)

echo Using Python: %PYTHON_CMD%
%PYTHON_CMD% --version

echo ╔═══════════════════════════════════════════════════════════════╗
echo ║         CampusPilot — ClassPilot Start Script                ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM ===== BACKEND =====
echo [1/3] Setting up backend virtual environment...
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv "%VENV_DIR%"
) else (
    echo Using existing virtual environment
)

echo Upgrading pip...
"%VENV_DIR%\Scripts\pip.exe" install --upgrade pip -q

echo Installing Python dependencies...
"%VENV_DIR%\Scripts\pip.exe" install -r "%ROOT_DIR%CampusPilot\requirements.txt"

echo Seeding database...
cd /d "%BACKEND_DIR%"
"%VENV_DIR%\Scripts\python.exe" scripts/seed.py

echo Starting FastAPI server on http://localhost:8000 ...
start "CampusPilot Backend" cmd /k "%VENV_DIR%\Scripts\python.exe -m uvicorn main:app --reload --port 8000"

timeout /t 3 >nul

REM ===== FRONTEND =====
echo.
echo [2/3] Setting up frontend...
cd /d "%FRONTEND_DIR%"
if not exist "node_modules" (
    echo Installing npm dependencies...
    npm install
) else (
    echo node_modules exists, skipping npm install
)

echo Starting Vite dev server on http://localhost:5173 ...
start "CampusPilot Frontend" cmd /k "npm run dev"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  CampusPilot is running!                                     ║
echo ║  • Frontend: http://localhost:5173                           ║
echo ║  • Backend API: http://localhost:8000                        ║
echo ║  • API Docs: http://localhost:8000/docs                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Press any key to stop servers and exit...
pause >nul

REM Cleanup
taskkill /f /fi "WINDOWTITLE eq CampusPilot Backend" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq CampusPilot Frontend" >nul 2>&1
echo Servers stopped.