from .text import normalize_text

def detect_work_mode(text: str | None) -> str:
    text = normalize_text(text)

    if not text:
        return "unknown"

    if "remoto" in text or "100% remoto" in text:
        return "remote"
    if "hibrido" in text:
        return "hybrid"
    if "presencial" in text:
        return "onsite"

    return "unknown"
