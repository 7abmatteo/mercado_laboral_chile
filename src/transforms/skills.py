from .text import normalize_text

def extract_skills(text: str | None, skill_catalog: set[str]) -> list[str]:
    text = normalize_text(text)
    if not text:
        return []

    found = {skill for skill in skill_catalog if skill in text}
    return sorted(found)
