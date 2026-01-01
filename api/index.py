# api/index.py
import sys
import os

# Add backend to path so we can import from it
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Import your FastAPI app
from main import app

# Vercel serverless handler
from mangum import Mangum

# Export handler for Vercel
handler = Mangum(app, lifespan="off")

# For Vercel Python runtime
def handler_function(event, context):
    return handler(event, context)