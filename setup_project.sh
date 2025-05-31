#!/bin/bash

# Exit immediately if any command fails
set -e

# Create virtual environment in the parent folder
echo "Creating virtual environment in ../.venv ..."
python3 -m venv ../.venv

# Activate the virtual environment
echo "Activating virtual environment ..."
source ../.venv/bin/activate

# Upgrade pip
echo "Upgrading pip ..."
pip install --upgrade pip

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt ..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found. Skipping dependency installation."
fi

# Install Playwright and browser binaries
echo "Installing Playwright ..."
pip install playwright
echo "Installing Playwright browser binaries ..."
playwright install

echo "✅ Setup complete! Virtual environment is ready in '../.venv'."

