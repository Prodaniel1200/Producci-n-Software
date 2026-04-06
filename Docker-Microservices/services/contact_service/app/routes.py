from flask import Blueprint, current_app, jsonify, request


contact_bp = Blueprint("contact_api", __name__)


@contact_bp.post("/api/contact")
def create_contact():
    payload = request.get_json(silent=True) or {}
    result = current_app.contact_service.create(payload.get("nombre", ""), payload.get("correo", ""), payload.get("asunto", ""), payload.get("mensaje", ""))
    return jsonify(result), (201 if result.get("ok") else 400)
