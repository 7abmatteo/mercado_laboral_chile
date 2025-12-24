from .text import normalize_text

REGION_MAP = {
    "santiago": "RM",
    "valparaiso": "V",
    "concepcion": "VIII",
}

def normalize_location(location_text: str | None) -> dict:
    text = normalize_text(location_text)

    city = None
    region = None

    if text:
        for key, reg in REGION_MAP.items():
            if key in text:
                city = key.capitalize()
                region = reg
                break

    return {
        "city": city,
        "region": region,
        "country": "CL"
    }
