import math
from copy import deepcopy
from typing import Any, Callable

PONENTES = [
    {
        "nombre": "Dra. Martinez",
        "pais": "Mexico",
        "bandera": "banderas/mexico.png",
        "titulo": "Innovacion tecnologica",
        "tipo": "Conferencia",
        "fecha": "2026-05-10",
        "hora": "09:00",
        "modalidad": "Presencial",
        "sede": "Claustro",
        "salon": "Auditorio 1",
    },
    {
        "nombre": "Ing. Perez",
        "pais": "Colombia",
        "bandera": "banderas/colombia.png",
        "titulo": "Innovacion tecnologica",
        "tipo": "Conferencia",
        "fecha": "2026-05-10",
        "hora": "10:00",
        "modalidad": "Presencial",
        "sede": "Claustro",
        "salon": "Auditorio 2",
    },
    {
        "nombre": "Dr. Lopez",
        "pais": "Argentina",
        "bandera": "banderas/argentina.png",
        "titulo": "Innovacion tecnologica",
        "tipo": "Conferencia",
        "fecha": "2026-05-10",
        "hora": "11:00",
        "modalidad": "Presencial",
        "sede": "Claustro",
        "salon": "Auditorio 3",
    },
    {
        "nombre": "Dr. Hans Muller",
        "pais": "Alemania",
        "bandera": "banderas/alemania.png",
        "titulo": "Innovacion tecnologica",
        "tipo": "Conferencia",
        "fecha": "2026-05-10",
        "hora": "12:00",
        "modalidad": "Presencial",
        "sede": "Claustro",
        "salon": "Auditorio 4",
    },
    {
        "nombre": "Dr. Jean Dupont",
        "pais": "Francia",
        "bandera": "banderas/francia.png",
        "titulo": "Innovacion tecnologica",
        "tipo": "Conferencia",
        "fecha": "2026-05-10",
        "hora": "13:00",
        "modalidad": "Presencial",
        "sede": "Claustro",
        "salon": "Auditorio 5",
    },
    {
        "nombre": "Ing. Carlos Silva",
        "pais": "Brasil",
        "bandera": "banderas/brasil.png",
        "titulo": "Innovacion tecnologica",
        "tipo": "Conferencia",
        "fecha": "2026-05-10",
        "hora": "14:00",
        "modalidad": "Presencial",
        "sede": "Claustro",
        "salon": "Auditorio 6",
    },
    {
        "nombre": "Dra. Sofia Rodriguez",
        "pais": "Panama",
        "bandera": "banderas/panama.png",
        "titulo": "Innovacion tecnologica",
        "tipo": "Conferencia",
        "fecha": "2026-05-10",
        "hora": "15:00",
        "modalidad": "Presencial",
        "sede": "Claustro",
        "salon": "Auditorio 7",
    },
]


def _build_event(ponente: dict[str, Any]):
    return {
        "fecha": ponente["fecha"],
        "hora": ponente["hora"],
        "tipo": ponente["tipo"],
        "titulo": ponente["titulo"],
        "ponente": {
            "nombre": ponente["nombre"],
            "pais": ponente["pais"],
            "bandera": ponente["bandera"],
        },
        "modalidad": ponente["modalidad"],
        "sede": ponente["sede"],
        "salon": ponente["salon"],
    }


def get_agenda(page: int = 1, per_page: int = 5):
    total_pages = max(1, math.ceil(len(PONENTES) / per_page))
    safe_page = min(max(page, 1), total_pages)
    start = (safe_page - 1) * per_page
    end = start + per_page
    ponentes = deepcopy(PONENTES[start:end])
    eventos = [_build_event(ponente) for ponente in ponentes]
    ponentes_ui = [
        {"nombre": p["nombre"], "pais": p["pais"], "bandera": p["bandera"]}
        for p in ponentes
    ]
    return {
        "page": safe_page,
        "per_page": per_page,
        "total_pages": total_pages,
        "ponentes": ponentes_ui,
        "eventos": eventos,
    }


def validate_ponencia_payload(payload: dict[str, Any]):
    required = ["nombre", "pais", "titulo", "fecha", "hora"]
    missing = [field for field in required if not str(payload.get(field, "")).strip()]
    if missing:
        return {
            "ok": False,
            "error": f"Campos obligatorios faltantes: {', '.join(missing)}",
        }
    return {"ok": True}


def create_ponencia(
    payload: dict[str, Any],
    notifier: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
):
    validation = validate_ponencia_payload(payload)
    if not validation["ok"]:
        return validation

    ponencia = {
        "nombre": payload["nombre"].strip(),
        "pais": payload["pais"].strip(),
        "bandera": payload.get("bandera", "banderas/mexico.png")
        or "banderas/mexico.png",
        "titulo": payload["titulo"].strip(),
        "tipo": payload.get("tipo", "Ponencia").strip() or "Ponencia",
        "fecha": payload["fecha"].strip(),
        "hora": payload["hora"].strip(),
        "modalidad": payload.get("modalidad", "Presencial").strip() or "Presencial",
        "sede": payload.get("sede", "Claustro").strip() or "Claustro",
        "salon": payload.get("salon", "Auditorio Nuevo").strip() or "Auditorio Nuevo",
    }
    PONENTES.append(ponencia)

    response = {
        "ok": True,
        "message": "Ponencia creada correctamente",
        "notification_status": "not_requested",
        "ponencia": deepcopy(ponencia),
    }

    if notifier:
        try:
            notify_result = notifier(
                {
                    "titulo": ponencia["titulo"],
                    "ponente_nombre": ponencia["nombre"],
                    "fecha": ponencia["fecha"],
                    "hora": ponencia["hora"],
                }
            )
            if notify_result.get("ok"):
                response["notification_status"] = "sent"
            else:
                response["notification_status"] = "degraded"
                response["warning"] = notify_result.get(
                    "error", "La notificacion no pudo procesarse"
                )
        except Exception:
            response["notification_status"] = "degraded"
            response["warning"] = (
                "La ponencia fue creada, pero el servicio de notificaciones no esta disponible"
            )

    return response
