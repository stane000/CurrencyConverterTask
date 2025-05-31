@echo off
echo === Activating virtual environment ===
call .venv\Scripts\activate.bat

echo === Running web converter tests ===
pytest -s -m calc

pause