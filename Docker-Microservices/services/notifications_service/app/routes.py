from datetime import UTC, datetime
from flask import Blueprint, jsonify, request


notifications_bp = Blueprint("notifications_api", __name__)


@notifications_bp.post("/api/notifications/ponencia-created")
def notify_ponencia_created():
    payload = request.get_json(silent=True) or {}
    required = ["titulo", "ponente_nombre"]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        return jsonify({"ok": False, "error": f"Campos faltantes: {', '.join(missing)}"}), 400

    return jsonify(
        {
            "ok": True,
            "event": "ponencia_created",
            "processed_at": datetime.now(UTC).isoformat(),
            "message": f"Notificacion procesada para {payload['ponente_nombre']}"
        }
    ), 202
