from datetime import datetime
from .job import normalize_job_title
from .salary import parse_salary
from .location import normalize_location
from .work_mode import detect_work_mode
from .skills import extract_skills
from .dates import normalize_dates

def build_staging_document(raw_doc: dict, skill_catalog: set[str]) -> dict:
    extraction_date = datetime.utcnow()

    job = normalize_job_title(raw_doc.get("cargo"))
    salary = parse_salary(raw_doc.get("salario"))
    location = normalize_location(raw_doc.get("ubicacion"))
    dates = normalize_dates(raw_doc.get("fecha_publicacion"), extraction_date)

    return {
        "job": job,
        "salary": salary,
        "location": location,
        "work_mode": detect_work_mode(raw_doc.get("descripcion")),
        "skills": extract_skills(raw_doc.get("descripcion"), skill_catalog),
        "dates": dates,
        "source": raw_doc.get("fuente"),
        "extracted_at": extraction_date
    }
