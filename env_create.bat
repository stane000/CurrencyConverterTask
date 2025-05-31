@echo off
REM Create a virtual environment in a folder named 'venv'
python -m venv venv

IF %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment.
    pause
    exit /b %ERRORLEVEL%
)

echo Virtual environment created successfully in the 'venv' folder.
