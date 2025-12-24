from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import hashlib
import time


# =========================
# Configuración general
# =========================

PORTAL_NAME = "computrabajo_chile"
BASE_URL = "https://cl.computrabajo.com/empleos-en-rmetropolitana"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MercadoLaboralBot/1.0)"
}

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "mercado_laboral_chile"
COLLECTION_NAME = "ofertas_raw"

REQUEST_DELAY = 2  # segundos entre requests (buena práctica)


# =========================
# Utilidades
# =========================

def generate_id(fuente: str, url: str) -> str:
    """
    Genera un ID estable a partir de fuente + URL
    """
    raw = f"{fuente}|{url}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def fetch_list_page(url: str) -> BeautifulSoup:
    """
    Descarga la página de listado y retorna el HTML parseado
    """
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_offers_list(soup: BeautifulSoup) -> list[str]:
    """
    Extrae las URLs de ofertas desde el listado
    """
    links = set()

    for a in soup.select('a[href^="/ofertas-de-trabajo/oferta"]'):
        href = a.get("href")
        if href:
            links.add("https://cl.computrabajo.com" + href)

    return list(links)


def fetch_offer_detail(url: str) -> dict:
    """
    Scrapea el detalle de una oferta (RAW)
    """
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    titulo = soup.select_one("h1")
    empresa = soup.select_one("a.fc_blue")
    ciudad = soup.select_one("span[itemprop='addressLocality']")
    descripcion = soup.select_one("div[itemprop='description']")

    return {
        "fuente": PORTAL_NAME,
        "url_oferta": url,

        "titulo_puesto": titulo.get_text(strip=True) if titulo else None,
        "empresa": empresa.get_text(strip=True) if empresa else None,

        "ubicacion": {
            "pais": "Chile",
            "region": None,
            "ciudad": ciudad.get_text(strip=True) if ciudad else None
        },

        "modalidad": None,
        "tipo_contrato": None,
        "jornada": None,

        "salario_min": None,
        "salario_max": None,
        "moneda": "CLP",

        "descripcion": descripcion.get_text("\n", strip=True) if descripcion else None,

        "fecha_publicacion": None,
        "fecha_scraping": datetime.now(timezone.utc),

        "estado_oferta": "activa",

        # Guardar HTML completo es típico en RAW
        "raw_html": str(soup)
    }


# =========================
# Ingesta principal
# =========================

def run_ingestion():
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION_NAME]

    soup = fetch_list_page(BASE_URL)
    offer_urls = parse_offers_list(soup)

    print(f"Ofertas encontradas en listado: {len(offer_urls)}")

    documentos = []
    inserted = 0

    for url in offer_urls:
        try:
            oferta = fetch_offer_detail(url)
            oferta["id_oferta"] = generate_id(oferta["fuente"], oferta["url_oferta"])
            documentos.append(oferta)
            inserted += 1
            time.sleep(REQUEST_DELAY)

        except Exception as e:
            print("========== ERROR ==========")
            print(f"URL: {url}")
            print(e)
            print("===========================")

    insertadas = 0

    for doc in documentos:
        result = collection.update_one(
            {"id_oferta": doc["id_oferta"]},
            {"$setOnInsert": doc},
            upsert=True
        )

        if result.upserted_id is not None:
            insertadas += 1

    print(f"Insertadas {insertadas} nuevas ofertas en '{COLLECTION_NAME}'")



if __name__ == "__main__":
    run_ingestion()


