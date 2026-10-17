"""
/api/datasets
=============
Lists every dataset currently available to the engine — the ones shipped
under data/cleaned/ plus anything a user has uploaded via /api/upload.
"""

from pathlib import Path
from fastapi import APIRouter

from app.utils import DATA_DIR, REALTIME_DIR, UPLOAD_DIR

router = APIRouter()


def _count_rows(path: Path) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            count = sum(1 for _ in f) - 1
            return max(count, 0)
    except Exception:
        return 0


def _describe(directory: Path, source: str):
    items = []
    if not directory.exists():
        return items
    for path in sorted(directory.glob("*.csv")):
        try:
            size_kb = round(path.stat().st_size / 1024, 1)
        except OSError:
            size_kb = None
        rows = _count_rows(path)

        # Determine clean status and corresponding cleaned filename
        is_raw = path.name.startswith("raw_")
        is_cleaned = ("cleaned" in path.name.lower() or source == "built-in") and not is_raw
        
        if is_cleaned:
            clean_filename = path.name
        elif is_raw:
            clean_filename = f"cleaned_{path.name[4:]}"
        else:
            clean_filename = f"cleaned_{path.name}"

        items.append({
            "name": path.name,
            "filename": path.name,
            "source": source,
            "type": source,
            "size_kb": size_kb,
            "rows": rows,
            "is_cleaned": is_cleaned,
            "clean_filename": clean_filename,
            "download_url": f"/api/download-cleaned?filename={clean_filename}",
            "download_json_url": f"/api/download-cleaned?filename={clean_filename}&format=json",
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
