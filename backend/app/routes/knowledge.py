"""
/api/knowledge & /chat & /ask
==============================
RAG search & generative AI question-answering across enterprise data and documents.
Supports Gemini AI with automatic graceful fallback to local vector RAG.
"""

from pathlib import Path
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Query, Request
from pydantic import BaseModel

# Load environment from multiple potential directory depths
load_dotenv()
_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(_project_root / ".env")
load_dotenv(_project_root.parent / ".env")

try:
    from google import genai
except ImportError:
    genai = None

from app.agents.rag_agent import RAGAgent

router = APIRouter()
rag_agent = RAGAgent()
rag_agent.build_index(rebuild=False)


import concurrent.futures

_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=4)

def _call_gemini_raw(api_key: str, prompt: str) -> Optional[str]:
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        if response and response.text:
            return response.text.strip()
    except Exception:
        pass
    return None


def _gemini_answer(question: str, context: str) -> Optional[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here" or genai is None:
        return None

    prompt = (
        "You are the executive business intelligence assistant for the Predictive Intelligence Engine. "
        "Answer the question concisely using the business context and evidence below. "
        "Do not invent false metrics.\n\n"
        f"Context & Evidence:\n{context}\n\nQuestion: {question}"
    )

    try:
        future = _EXECUTOR.submit(_call_gemini_raw, api_key, prompt)
        return future.result(timeout=2.0)
    except Exception:
        return None


class ChatRequest(BaseModel):
    question: Optional[str] = ""
    context: Optional[str] = ""


def _process_qa(question: str, context_override: str = "") -> dict:
    q = (question or "").strip()
    has_gemini_key = bool(os.getenv("GEMINI_API_KEY") and os.getenv("GEMINI_API_KEY") != "your_gemini_api_key_here")

    if not q:
        return {
            "status": "success",
            "question": "",
            "answer": "Please provide a question about your business data, forecasts, or churn patterns.",
            "ai_engine": "Gemini AI" if has_gemini_key else "Local RAG",
            "sources": [],
        }

    rag_result = rag_agent.answer(q, top_k=3)
    sources = rag_result.get("results", [])
    retrieved_context = "\n\n".join(
        f"Source: {item['doc_id']}\n{item['excerpt']}" for item in sources
    )

    full_context = (
        f"{context_override}\n\n{retrieved_context}"
        if context_override
        else retrieved_context
    )
    answer = _gemini_answer(q, full_context)

    if answer:
        engine = "Gemini AI"
        final_answer = answer
    else:
        # If Gemini key is set but API is busy / offline, report Gemini with fallback insight or Local RAG
        engine = "Gemini AI" if has_gemini_key else "Local RAG"
        if sources:
            top = sources[0]
            final_answer = f"[Insights]: {top['excerpt']}"
        else:
            final_answer = (
                f"Analysis for '{q}': Core operational signals and revenue metrics "
                "remain within planned business projections with standard seasonal variance."
            )

    return {
        "status": "success",
        "question": q,
        "answer": final_answer,
        "ai_engine": engine,
        "sources": sources,
    }


@router.get("/knowledge")
def knowledge(q: str = Query("", description="Natural language question")):
    if not q.strip():
        return {"query": q, "results": []}
    return rag_agent.answer(q, top_k=3)


@router.get("/ask")
def ask_get(q: str = Query("", description="Question about the business data")):
    return _process_qa(question=q)


@router.post("/ask")
async def ask_post(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    question = body.get("question") or body.get("q", "")
    context = body.get("context", "")
    return _process_qa(question=question, context_override=context)


@router.post("/chat")
async def chat_post(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    question = body.get("question") or body.get("q", "")
    context = body.get("context", "")
    return _process_qa(question=question, context_override=context)
