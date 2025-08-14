@echo off
echo ========================================
echo    QTrace - Quantum State Visualizer
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment.
        echo Please ensure Python is installed and in your PATH.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install requirements if needed
if not exist ".venv\Lib\site-packages\streamlit" (
    echo Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install requirements.
        pause
        exit /b 1
    )
)

REM Run QTrace
echo.
echo Starting QTrace...
echo.
echo The application will open in your default web browser.
echo If it doesn't open automatically, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application.
echo.

streamlit run app.py

pause
