import requests
from flask import Blueprint, current_app, jsonify, request
from .service import create_ponencia, get_agenda


agenda_bp = Blueprint("agenda_api", __name__)


@agenda_bp.get("/api/agenda")
def agenda():
    return jsonify(
        get_agenda(
            page=request.args.get("page", 1, type=int),
            per_page=request.args.get("per_page", 5, type=int),
        )
    )


@agenda_bp.post("/api/ponentes")
def create_ponente():
    payload = request.get_json(silent=True) or {}

    def notifier(notification_payload):
        response = requests.post(
            f"{current_app.config['NOTIFICATIONS_SERVICE_URL']}/api/notifications/ponencia-created",
            json=notification_payload,
            timeout=current_app.config["REQUEST_TIMEOUT"],
        )
        response.raise_for_status()
        return response.json()

    result = create_ponencia(payload, notifier=notifier)
    status = 201 if result.get("ok") else 400
    return jsonify(result), status
