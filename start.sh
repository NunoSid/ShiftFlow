#!/usr/bin/env bash
set -euo pipefail

echo "Starting ShiftFlow..."

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  echo ".env not found."
  read -r -p "Create .env from .env.example? (y/N): " create_env
  if [[ "${create_env:-}" =~ ^[yY]$ ]]; then
    cp ".env.example" ".env"
    echo "Created .env from .env.example."
  else
    echo "Continuing without .env."
  fi
fi

if [ -f ".env" ]; then
  set -a
  . ".env"
  set +a
fi

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

echo "Installing dependencies..."
. .venv/bin/activate
pip install -r requirements.txt

HOST="${SHIFTFLOW_HOST:-0.0.0.0}"
PORT="${SHIFTFLOW_PORT:-8010}"

echo "Starting backend (http://localhost:${PORT})..."
uvicorn backend.app.main:app --reload --host "${HOST}" --port "${PORT}"
