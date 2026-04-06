from flask import Blueprint, current_app, jsonify, request


auth_bp = Blueprint("auth_api", __name__)


@auth_bp.post("/api/auth/login")
def login():
    payload = request.get_json(silent=True) or {}
    result = current_app.auth_service.login(payload.get("email", ""), payload.get("password", ""))
    return jsonify(result), (200 if result.get("ok") else 401)


@auth_bp.post("/api/auth/register")
def register():
    payload = request.get_json(silent=True) or {}
    result = current_app.auth_service.register(payload.get("name", ""), payload.get("email", ""), payload.get("password", ""))
    return jsonify(result), (201 if result.get("ok") else 400)
