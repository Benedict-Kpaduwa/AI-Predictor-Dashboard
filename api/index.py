# api/index.py
import sys
import os

# Add backend to path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import your FastAPI app
from main import app

# Vercel serverless handler
from mangum import Mangum
handler = Mangum(app, lifespan="off")