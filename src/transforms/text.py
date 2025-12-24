import unicodedata
import re

def normalize_text(text: str | None) -> str | None:
    if not text:
        return None

    text = text.lower().strip()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"\s+", " ", text)

    return text
