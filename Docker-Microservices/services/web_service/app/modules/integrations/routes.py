from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required
from requests.exceptions import RequestException

from ...clients import integrations_client


integrations_bp = Blueprint("integrations", __name__)


@integrations_bp.route("/api/coniiti")
@login_required
def api_coniiti():
    try:
        return jsonify(integrations_client.get_coniiti_data())
    except RequestException:
        return jsonify({"error": "Servicio de integraciones no disponible"}), 503


@integrations_bp.route("/coniiti")
@login_required
def ver_coniiti():
    datos = {"status": "error", "error": "Servicio no disponible"}
    try:
        datos = integrations_client.get_coniiti_data()
    except RequestException:
        pass
    return render_template("coniiti.html", datos=datos)


@integrations_bp.route("/login-outlook")
def login_outlook():
    try:
        redirect_uri = url_for("integrations.callback", _external=True)
        data = integrations_client.get_outlook_login_url(redirect_uri)
        if not data.get("ok"):
            return redirect(url_for("public.inicio"))
        return redirect(data["auth_url"])
    except RequestException:
        return redirect(url_for("public.inicio"))


@integrations_bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return redirect(url_for("public.inicio"))
    try:
        redirect_uri = url_for("integrations.callback", _external=True)
        result = integrations_client.exchange_outlook_code(code, redirect_uri)
        if result.get("ok"):
            session["ms_token"] = result.get("access_token")
    except RequestException:
        pass
    return redirect(url_for("public.inicio"))
