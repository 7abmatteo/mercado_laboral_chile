from datetime import datetime, timedelta
from .text import normalize_text

def normalize_dates(posted_text: str | None, extraction_date: datetime) -> dict:
    text = normalize_text(posted_text)

    published_at = extraction_date

    if text:
        if "hoy" in text:
            published_at = extraction_date
        elif "ayer" in text:
            published_at = extraction_date - timedelta(days=1)

    return {
        "published_at": published_at,
        "last_seen_at": extraction_date
    }
