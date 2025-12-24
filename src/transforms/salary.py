import re
from .text import normalize_text

def parse_salary(salary_text: str | None) -> dict:
    text = normalize_text(salary_text)

    if not text:
        return {
            "min_clp": None,
            "max_clp": None,
            "currency": "CLP",
            "period": "monthly",
            "salary_present": False
        }

    numbers = [int(n.replace(".", "")) for n in re.findall(r"\d{1,3}(?:\.\d{3})+", text)]

    if not numbers:
        return {
            "min_clp": None,
            "max_clp": None,
            "currency": "CLP",
            "period": "monthly",
            "salary_present": False
        }

    return {
        "min_clp": min(numbers),
        "max_clp": max(numbers),
        "currency": "CLP",
        "period": "monthly",
        "salary_present": True
    }
