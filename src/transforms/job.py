from .text import normalize_text

SENIORITY_KEYWORDS = {
    "junior": ["junior", "jr", "trainee"],
    "senior": ["senior", "sr"],
    "semi-senior": ["semi senior", "ssr"]
}

ROLE_GROUPS = {
    "data": ["analista de datos", "data analyst", "data analytics"],
    "bi": ["business intelligence", "bi"],
    "ml": ["machine learning", "ml"],
}

def normalize_job_title(title_raw: str | None) -> dict:
    title = normalize_text(title_raw)

    seniority = "unspecified"
    for level, keywords in SENIORITY_KEYWORDS.items():
        if title and any(k in title for k in keywords):
            seniority = level
            break

    role_group = "other"
    for group, keywords in ROLE_GROUPS.items():
        if title and any(k in title for k in keywords):
            role_group = group
            break

    return {
        "title": title,
        "role_group": role_group,
        "seniority": seniority
    }
