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
APP_PID=$!
python chat.py &
CHAT_PID=$!

echo "Starting frontend"
cd "$SCRIPT_DIR/frontend_mm" || exit 1
npm run dev &
FRONTEND_PID=$!

cleanup() {
    echo "Stopping all processes..."
    
    if ps -p $APP_PID > /dev/null; then
        echo "Killing backend app process: $APP_PID"
        kill $APP_PID
    fi
    
    if ps -p $CHAT_PID > /dev/null; then
        echo "Killing backend chat process: $CHAT_PID"
        kill $CHAT_PID
    fi
    
    if ps -p $FRONTEND_PID > /dev/null; then
        echo "Killing frontend process: $FRONTEND_PID"
        kill $FRONTEND_PID
    fi
    
    echo "All processes stopped"
    exit 0
}

# Set up trap for Ctrl+C and other termination signals
trap cleanup SIGINT SIGTERM

# Wait for all processes
wait $APP_PID
wait $CHAT_PID
wait $FRONTEND_PID