import requests
from bs4 import BeautifulSoup


def obtener_datos_coniiti():
    url = "https://coniiti.com/"
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "es-ES,es;q=0.9"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        titulos = [
            h.get_text(strip=True)
            for h in soup.find_all(["h1", "h2"])
            if h.get_text(strip=True)
        ]
        parrafos = [
            p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)
        ]
        return {"titulos": titulos[:5], "parrafos": parrafos[:5], "status": "ok"}
    except requests.exceptions.RequestException as exc:
        return {
            "error": "No se pudo conectar con el sitio",
            "detalle": str(exc),
            "status": "error",
        }
