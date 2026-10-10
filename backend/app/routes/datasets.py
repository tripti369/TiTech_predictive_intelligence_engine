"""
/api/datasets
=============
Lists every dataset currently available to the engine — the ones shipped
under data/cleaned/ plus anything a user has uploaded via /api/upload.
"""

from fastapi import APIRouter

from app.utils import DATA_DIR, REALTIME_DIR, UPLOAD_DIR

router = APIRouter()


from pathlib import Path

def _count_rows(path: Path) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            count = sum(1 for _ in f) - 1
            return max(count, 0)
    except Exception:
        return 0


def _describe(directory, source: str):
    items = []
    if not directory.exists():
        return items
    for path in sorted(directory.glob("*.csv")):
        try:
            size_kb = round(path.stat().st_size / 1024, 1)
        except OSError:
            size_kb = None
        rows = _count_rows(path)
        items.append({
            "name": path.name,
            "filename": path.name,
            "source": source,
            "type": source,
            "size_kb": size_kb,
            "rows": rows,
        })
    return items


@router.get("/datasets")
def datasets():
    return {
        "datasets": (
            _describe(DATA_DIR, "built-in")
            + _describe(UPLOAD_DIR, "uploaded")
            + _describe(REALTIME_DIR, "realtime")
        ),
    }
