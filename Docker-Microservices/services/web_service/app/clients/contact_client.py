from flask import current_app
from .http import post_json


def send_contact_message(nombre, correo, asunto, mensaje):
    return post_json(
        f"{current_app.config['CONTACT_SERVICE_URL']}/api/contact",
        {
            "nombre": nombre,
            "correo": correo,
            "asunto": asunto,
            "mensaje": mensaje,
        },
    )
