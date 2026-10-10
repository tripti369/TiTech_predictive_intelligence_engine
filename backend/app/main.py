"""
main.py
=======
FastAPI application entrypoint for the Predictive Intelligence Engine.

Run with:
    python backend/run.py
Or:
    uvicorn backend.app.main:app --reload --port 8000
Or:
    uvicorn app:app --reload --port 8000
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# Load environment configuration
load_dotenv()
_BACKEND_DIR = Path(__file__).resolve().parent.parent        # …/backend
_PROJECT_ROOT = _BACKEND_DIR.parent                          # …/
load_dotenv(_PROJECT_ROOT / ".env")

from app.database import init_db
from app.routes import (
    predict,
    analysis,
    scenario,
    upload,
    knowledge,
    history,
    datasets,
    realtime,
)

_FRONTEND_DIR = _PROJECT_ROOT / "frontend"

app = FastAPI(
    title="Predictive Intelligence Engine API",
    description="Real-data backend powering forecasting, churn/attrition analysis, "
                "Monte Carlo scenario simulation, CSV upload, and agentic knowledge retrieval.",
    version="1.0.0",
)

cors_origins = os.getenv("CORS_ORIGINS", "*")
allow_origins = ["*"] if cors_origins.strip() == "*" else [o.strip() for o in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


# ── Mount routes under BOTH /api and root prefixes for universal client support ──
all_routers = [
    (predict.router, "Predict"),
    (analysis.router, "Analysis"),
    (scenario.router, "Scenario"),
    (upload.router, "Upload"),
    (knowledge.router, "Knowledge / RAG"),
    (history.router, "History"),
    (datasets.router, "Datasets"),
    (realtime.router, "Realtime"),
]

for router_obj, tag in all_routers:
    app.include_router(router_obj, prefix="/api", tags=[tag])
    app.include_router(router_obj, prefix="", tags=[tag])


def _get_health_data():
    has_gemini = bool(os.getenv("GEMINI_API_KEY") and os.getenv("GEMINI_API_KEY") != "your_gemini_api_key_here")
    return {
        "status": "ok",
        "message": "Predictive Intelligence Engine API is running",
        "version": "1.0.0",
        "ai_engine": "Gemini AI" if has_gemini else "Local RAG",
        "gemini_configured": has_gemini,
        "features": [
            "analysis",
            "forecasting",
            "scenarios",
            "rag",
            "decisions",
            "realtime",
            "upload",
        ],
        "api": "/docs",
        "docs": "/docs",
    }


@app.get("/health")
@app.get("/api/health")
def health():
    return _get_health_data()


# ── Serve frontend assets & smart root handler ────────────────────────
if _FRONTEND_DIR.is_dir():
    for sub in ("css", "js", "images", "assets"):
        sub_dir = _FRONTEND_DIR / sub
        if sub_dir.is_dir():
            app.mount(f"/{sub}", StaticFiles(directory=str(sub_dir)), name=sub)

    @app.get("/")
    def root(request: Request):
        accept = request.headers.get("accept", "")
        # If API client explicitly requests JSON without text/html, return JSON health
        if "application/json" in accept and "text/html" not in accept:
            return JSONResponse(content=_get_health_data())
        index_path = _FRONTEND_DIR / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return JSONResponse(content=_get_health_data())

    @app.get("/index.html")
    def serve_index_html():
        index_path = _FRONTEND_DIR / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return JSONResponse(content=_get_health_data())
else:
    @app.get("/")
    def root():
        return _get_health_data()

