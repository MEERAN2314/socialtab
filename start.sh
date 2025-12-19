#!/bin/bash

# Start script for Render deployment
echo "🚀 Starting SocialTab..."

# Get port from environment or default to 8000
PORT=${PORT:-8000}

echo "📡 Starting server on port $PORT..."

# Start uvicorn
exec uvicorn main:app --host 0.0.0.0 --port $PORT
