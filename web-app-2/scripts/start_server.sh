#!/bin/bash
# Before running the script, make it executable: chmod +x start_server.sh
# Then run the server: ./start_server.sh

# Navigate to your app directory
cd /path/to/your/flask/app

# Activate your virtual environment if you have one
# source venv/bin/activate

# Start gunicorn server
gunicorn -w 4 -b 0.0.0.0:8000 your_flask_app:app
