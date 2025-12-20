from datetime import datetime, date, timezone
from pymongo import MongoClient
from typing import Any


# =========================
# Normalización de fechas
# =========================

def normalize_dates(value: Any) -> Any:
    """
    Convierte recursivamente datetime.date -> datetime.datetime (UTC)
    en dicts, listas y valores simples.
    """
    if isinstance(value, date) and not isinstance(value, datetime):
        return datetime(value.year, value.month, value.day, tzinfo=timezone.utc)

    elif isinstance(value, dict):
        return {k: normalize_dates(v) for k, v in value.items()}

    elif isinstance(value, list):
        return [normalize_dates(v) for v in value]

    return value


# =========================
# Validación mínima
# =========================

def validate_oferta(o: dict) -> bool:
    """
    Validación mínima para evitar basura en la base.
    """
    required_fields = [
        "fuente",
        "puesto",
        "fecha_publicacion",
        "fecha_ingesta",
    ]

    for field in required_fields:
        if o.get(field) is None:
            return False

    # Validaciones simples de negocio
    if o.get("salario_min") is not None and o["salario_min"] < 0:
        return False

    if o.get("salario_max") is not None and o["salario_max"] < 0:
        return False

    return True


# =========================
# Conexión MongoDB
# =========================

client = MongoClient("mongodb://localhost:27017/")
db = client["mercado_laboral_chile"]
collection = db["ofertas_raw"]


# =========================
# Datos de ejemplo
# =========================

now_utc = datetime.now(timezone.utc)

ofertas = [
    {
        "fuente": "portal_empleo_chile",
        "puesto": "Analista de Datos",
        "empresa": "Empresa X",
        "ubicacion": "Santiago",
        "modalidad": "híbrido",
        "salario_min": 1200000,
        "salario_max": 1600000,
        "moneda": "CLP",
        "skills": ["Python", "SQL", "Excel"],
        "fecha_publicacion": date(2025, 1, 10),
        "fecha_ingesta": now_utc,
    },
    {
        "fuente": "portal_empleo_chile",
        "puesto": "Científico de Datos Jr",
        "empresa": None,
        "ubicacion": "Chile",
        "modalidad": "remoto",
        "salario_min": None,
        "salario_max": None,
        "moneda": "CLP",
        "skills": ["Python", "Pandas", "Machine Learning"],
        "fecha_publicacion": date(2025, 1, 8),
        "fecha_ingesta": now_utc,
    },
]


# =========================
# Pipeline de ingesta
# =========================

# 1. Normalizar fechas (blindaje total)
ofertas = [normalize_dates(o) for o in ofertas]

# 2. Validar
ofertas_validas = [o for o in ofertas if validate_oferta(o)]

if not ofertas_validas:
    raise ValueError("No hay ofertas válidas para insertar")

# 3. Insertar
resultado = collection.insert_many(ofertas_validas)

print(f"Documentos insertados: {len(resultado.inserted_ids)}")
