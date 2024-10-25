#!/bin/bash

echo "Running all consoles..."

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # macOS or Linux
    echo "Starting python venv..."
    # start venv
    python -m venv .venv
    source .venv/bin/activate

elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash or WSL)
    echo "Starting python venv..."
    # start venv
    python -m venv .venv
    source .venv/Scripts/activate

fi

# Check if activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Virtual environment activation failed"
    exit 1
fi

echo "python venv started"

echo "installing dependencies backend"
cd "$SCRIPT_DIR/backend_mm" || exit 1
pip install -r requirements.txt

echo "installing dependencies frontend"
cd "$SCRIPT_DIR/frontend_mm" || exit 1
npm i