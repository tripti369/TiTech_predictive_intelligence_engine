"""
main.py
=======
Root Application Entrypoint for the Predictive Intelligence Engine.

Usage:
    python main.py             # Starts FastAPI server on port 8000 (or $PORT)
    uvicorn main:app --reload  # Starts ASGI server with hot-reload
"""

import os
import sys
from pathlib import Path

# Ensure backend directory is in sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent
_BACKEND_DIR = _PROJECT_ROOT / "backend"
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

# Import the canonical FastAPI application
from app.main import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Predictive Intelligence Engine running at http://0.0.0.0:{port}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)