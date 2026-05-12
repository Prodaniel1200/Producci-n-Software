from flask import current_app
from .http import get_json, post_json


def get_agenda(page=1, per_page=5):
    return get_json(
        f"{current_app.config['AGENDA_SERVICE_URL']}/api/agenda",
        {"page": page, "per_page": per_page},
    )


def create_ponencia(payload):
    return post_json(
        f"{current_app.config['AGENDA_SERVICE_URL']}/api/ponentes", payload
    )
