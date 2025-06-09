@echo off
echo === Activating virtual environment ===
call .venv\Scripts\activate.bat

echo === Running web converter tests ===
pytest -s -m all_converters_amount

pause