#!/usr/bin/env bash
set -e
set -x

echo "Creating virtual environment..."
python -m venv venv

echo "Activating virtual environment..."
source venv/Scripts/activate || source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
python -m playwright install

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
