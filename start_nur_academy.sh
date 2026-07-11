#!/bin/bash

# Launch Nur Academy: Full-Stack Islamiyat Prep System
# Usage: ./start_nur_academy.sh

# Exit on any error
set -e

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# Function to clean up background processes on exit
cleanup() {
    echo ""
    echo "Stopping Nur Academy..."
    kill $BACKEND_PID 2>/dev/null || true
    exit
}

# Trap Ctrl+C (SIGINT) and SIGTERM
trap cleanup SIGINT SIGTERM

echo "🚀 Starting Nur Academy System..."

# 1. Start Backend (FastAPI)
echo "Starting Backend (FastAPI) on http://127.0.0.1:8000..."
"$PROJECT_ROOT/venv/bin/python3" "$PROJECT_ROOT/backend/main.py" > backend.log 2>&1 &
BACKEND_PID=$!

# Wait a moment for backend to initialize
sleep 2

# Check if backend is actually running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Error: Backend failed to start. Check backend.log for details."
    exit 1
fi

# 2. Start Frontend (Next.js/Vite)
echo "Starting Frontend (Vite) on http://localhost:5173..."
cd "$PROJECT_ROOT/nur-academy"
npm run dev

# If npm run dev exits, cleanup
cleanup
