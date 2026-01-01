#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "=========================================="
echo "Installing Python dependencies..."
echo "=========================================="
pip install --upgrade pip
pip install -r requirements.txt

echo "=========================================="
echo "Building Frontend..."
echo "=========================================="
cd frontend

# Install Node.js dependencies
if command -v npm &> /dev/null; then
    echo "Installing frontend dependencies with npm..."
    npm install
    echo "Building frontend..."
    npm run build
else
    echo "Error: npm not found"
    exit 1
fi

cd ..

echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="

