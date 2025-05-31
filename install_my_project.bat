@echo off
echo === Creating virtual environment ===
call env_create.bat

echo === Installing packages ===
call env_packages.bat

echo === Installing Playwright ===
playwright install

echo === Setup complete ===
pause
