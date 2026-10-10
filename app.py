"""
Predictive Intelligence Engine — Root Application Entrypoint
============================================================
Exposes FastAPI app for:
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
Or:
    python app.py
"""

import sys
from pathlib import Path

_backend = str(Path(__file__).resolve().parent / "backend")
if _backend in sys.path:
    sys.path.remove(_backend)
sys.path.insert(0, _backend)

# Ensure 'app' refers to the backend package, not this root file module
if "app" in sys.modules and not hasattr(sys.modules["app"], "__path__"):
    del sys.modules["app"]

from app.main import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
