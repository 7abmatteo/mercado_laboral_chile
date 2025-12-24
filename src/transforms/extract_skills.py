import re

SKILLS_MAP = {
    "python": ["python"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "excel": ["excel"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "machine learning": ["machine learning", "ml"],
    "etl": ["etl"],
    "docker": ["docker"],
    "git": ["git", "github"],
}

def extract_skills_from_text(text: str) -> list[str]:
    if not text:
        return []

    text = text.lower()
    found = set()

    for skill, variants in SKILLS_MAP.items():
        for v in variants:
            pattern = r"\b" + re.escape(v) + r"\b"
            if re.search(pattern, text):
                found.add(skill)

    return sorted(found)



def transform_raw_to_staging(raw_collection, staging_collection):
    cursor = raw_collection.find()

    docs = []
    for o in cursor:
        skills = extract_skills_from_text(o.get("descripcion"))

        docs.append({
            "id_oferta": str(o["_id"]),
            "fuente": o.get("fuente"),
            "titulo_puesto": o.get("titulo_puesto"),
            "empresa": o.get("empresa"),
            "ciudad": o.get("ubicacion", {}).get("ciudad"),
            "skills": skills,
            "fecha_scraping": o.get("fecha_scraping"),
        })

    if docs:
        staging_collection.insert_many(docs)

