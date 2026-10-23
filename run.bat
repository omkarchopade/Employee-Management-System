@echo off
TITLE Employee Management System Setup & Run
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not added to PATH. Please install Python first.
    pause
    exit /b
)

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Initializing database and starting application...
python main.py

pause