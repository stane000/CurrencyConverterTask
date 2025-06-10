#!/bin/bash

# Exit on any error and catch piped failures
set -euo pipefail

# Ensure Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it and rerun this script."
    exit 1
fi

# Define the venv directory
VENV_DIR=".venv"

# Create virtual environment
echo "🔧 Creating virtual environment in '$VENV_DIR' ..."
python3 -m venv "$VENV_DIR"

# Activate virtual environment
echo "⚙️ Activating virtual environment ..."
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "⬆️ Upgrading pip ..."
pip install --upgrade pip

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing packages from requirements.txt ..."
    pip install -r requirements.txt
else
    echo "📁 No requirements.txt found. Skipping package installation."
fi

# Install Playwright and browser binaries
echo "🎭 Installing Playwright ..."
pip install playwright

echo "🌐 Installing Playwright browser binaries ..."
playwright install

echo "✅ Setup complete!"
echo "👉 Virtual environment is active. To use it later, run:"
echo "   source $VENV_DIR/bin/activate"

