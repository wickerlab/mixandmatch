echo "Running all consoles..."

if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # macOS or Linux
    echo "Starting python venv..."
    # start venv
    source /venv/bin/activate


elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash or WSL)
    echo "Starting python venv..."
    # start venv
    .venv\\Scripts\\activate

fi

echo "python venv started"

echo "starting backend"
cd backend_mm
python app.py &
python chat.py &

echo "starting frontend"
cd ../frontend_mm
npm run dev