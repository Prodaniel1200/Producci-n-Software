import requests
from bs4 import BeautifulSoup

URL_CONFER = "https://coniiti.com/"  # Página oficial

def obtener_eventos_coniiti():
    eventos = []
    try:
        response = requests.get(URL_CONFER, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Cada bloque de evento en el HTML
        for bloque in soup.select("div.evento"):
            titulo = bloque.select_one("h3.titulo").get_text(strip=True) if bloque.select_one("h3.titulo") else "Sin título"
            tipo = bloque.select_one("span.tipo").get_text(strip=True) if bloque.select_one("span.tipo") else "Desconocido"
            ponente = bloque.select_one("span.ponente").get_text(strip=True) if bloque.select_one("span.ponente") else "Desconocido"
            pais = bloque.select_one("span.pais").get_text(strip=True) if bloque.select_one("span.pais") else "Desconocido"
            fecha = bloque.select_one("span.fecha").get_text(strip=True) if bloque.select_one("span.fecha") else "Sin fecha"
            hora = bloque.select_one("span.hora").get_text(strip=True) if bloque.select_one("span.hora") else "Sin hora"

            eventos.append({
                "titulo": titulo,
                "tipo": tipo,
                "ponente": ponente,
                "pais": pais,
                "fecha": fecha,
                "hora": hora
            })
    except Exception as e:
        print("Error al obtener eventos:", e)

    return eventos
