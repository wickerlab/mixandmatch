#!/bin/bash

echo "Running all consoles..."

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # macOS or Linux
    echo "Starting python venv..."
    # Check if venv exists in project directory
    if [ -d "$SCRIPT_DIR/venv" ]; then
        source "$SCRIPT_DIR/venv/bin/activate"
    elif [ -d "$SCRIPT_DIR/.venv" ]; then
        source "$SCRIPT_DIR/.venv/bin/activate"
    else
        echo "Error: Virtual environment not found in $SCRIPT_DIR"
        echo "Please create a virtual environment first using:"
        echo "python -m venv venv"
        exit 1
    fi

elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash or WSL)
    echo "Starting python venv..."
    # Check if venv exists in project directory
    if [ -d "$SCRIPT_DIR/venv" ]; then
        source "$SCRIPT_DIR/venv/Scripts/activate"
    elif [ -d "$SCRIPT_DIR/.venv" ]; then
        source "$SCRIPT_DIR/.venv/Scripts/activate"
    else
        echo "Error: Virtual environment not found in $SCRIPT_DIR"
        echo "Please create a virtual environment first using:"
        echo "python -m venv venv"
        exit 1
    fi
fi

# Check if activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Virtual environment activation failed"
    exit 1
fi

echo "Python venv started successfully"

echo "Starting backend"
cd "$SCRIPT_DIR/backend_mm" || exit 1
python app.py &
python chat.py &

echo "Starting frontend"
cd "$SCRIPT_DIR/frontend_mm" || exit 1
npm run dev