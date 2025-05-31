#!/bin/bash

echo "=== Activating virtual environment ==="
source .venv/bin/activate

echo "=== Running web converter tests ==="
pytest -s -m web

# Pause equivalent (optional): wait for Enter before closing
read -p "Press Enter to continue..."

