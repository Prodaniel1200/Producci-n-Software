import math

PONENTES = [
    {"nombre": "Dra. Martínez", "pais": "México", "bandera": "banderas/mexico.png"},
    {"nombre": "Ing. Pérez", "pais": "Colombia", "bandera": "banderas/colombia.png"},
    {"nombre": "Dr. López", "pais": "Argentina", "bandera": "banderas/argentina.png"},
    {"nombre": "Dr. Hans Müller", "pais": "Alemania", "bandera": "banderas/alemania.png"},
    {"nombre": "Dr. Jean Dupont", "pais": "Francia", "bandera": "banderas/francia.png"},
    {"nombre": "Ing. Carlos Silva", "pais": "Brasil", "bandera": "banderas/brasil.png"},
    {"nombre": "Dra. Sofía Rodríguez", "pais": "Panamá", "bandera": "banderas/panama.png"},
    {"nombre": "Dr. Ana Torres", "pais": "México", "bandera": "banderas/mexico.png"},
    {"nombre": "Dr. Felipe Gómez", "pais": "Colombia", "bandera": "banderas/colombia.png"},
    {"nombre": "Dr. Laura Sánchez", "pais": "Argentina", "bandera": "banderas/argentina.png"},
    {"nombre": "Dr. Klaus Weber", "pais": "Alemania", "bandera": "banderas/alemania.png"},
    {"nombre": "Dr. Marie Dubois", "pais": "Francia", "bandera": "banderas/francia.png"},
    {"nombre": "Dr. Pedro Almeida", "pais": "Brasil", "bandera": "banderas/brasil.png"},
    {"nombre": "Dr. Ricardo Castillo", "pais": "Panamá", "bandera": "banderas/panama.png"},
]


def get_agenda(page: int = 1, per_page: int = 5):
    total_pages = max(1, math.ceil(len(PONENTES) / per_page))
    start = (page - 1) * per_page
    end = start + per_page
    ponentes = PONENTES[start:end]
    eventos = []
    for i, ponente in enumerate(ponentes):
        eventos.append({
            "fecha": "2026-05-10",
            "hora": f"{9 + i}:00",
            "tipo": "Conferencia",
            "titulo": "Innovación tecnológica",
            "ponente": ponente,
            "modalidad": "Presencial",
            "sede": "Claustro",
            "salon": f"Auditorio {i + 1}",
        })
    return {"page": page, "per_page": per_page, "total_pages": total_pages, "ponentes": ponentes, "eventos": eventos}
