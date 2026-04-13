from flask import Blueprint, current_app, jsonify, request

from .providers.coniiti_provider import obtener_datos_coniiti
from .providers.outlook_provider import build_msal_app


integrations_bp = Blueprint("integrations_api", __name__)


@integrations_bp.get("/api/integrations/coniiti")
@integrations_bp.get("/api/coniiti")
def coniiti():
    return jsonify(obtener_datos_coniiti())


@integrations_bp.get("/api/integrations/outlook/login-url")
@integrations_bp.get("/api/outlook/login-url")
def outlook_login_url():
    redirect_uri = request.args.get("redirect_uri", "")
    if not all([
        current_app.config["MS_CLIENT_ID"],
        current_app.config["MS_CLIENT_SECRET"],
        current_app.config["MS_TENANT_ID"],
        redirect_uri,
    ]):
        return jsonify({"ok": False, "error": "Outlook no está configurado"}), 400
    msal_app = build_msal_app(
        current_app.config["MS_CLIENT_ID"],
        current_app.config["MS_CLIENT_SECRET"],
        current_app.config["MS_TENANT_ID"],
    )
    auth_url = msal_app.get_authorization_url(current_app.config["MS_SCOPE"], redirect_uri=redirect_uri)
    return jsonify({"ok": True, "auth_url": auth_url})


@integrations_bp.post("/api/integrations/outlook/exchange-code")
@integrations_bp.post("/api/outlook/exchange-code")
def exchange_code():
    payload = request.get_json(silent=True) or {}
    code = payload.get("code", "")
    redirect_uri = payload.get("redirect_uri", "")
    if not all([
        current_app.config["MS_CLIENT_ID"],
        current_app.config["MS_CLIENT_SECRET"],
        current_app.config["MS_TENANT_ID"],
        code,
        redirect_uri,
    ]):
        return jsonify({"ok": False, "error": "Solicitud inválida o configuración faltante"}), 400
    msal_app = build_msal_app(
        current_app.config["MS_CLIENT_ID"],
        current_app.config["MS_CLIENT_SECRET"],
        current_app.config["MS_TENANT_ID"],
    )
    result = msal_app.acquire_token_by_authorization_code(
        code,
        current_app.config["MS_SCOPE"],
        redirect_uri=redirect_uri,
    )
    if "access_token" not in result:
        return jsonify({"ok": False, "error": result.get("error_description", "No se pudo obtener el token")}), 400
    return jsonify({"ok": True, "access_token": result["access_token"]})
