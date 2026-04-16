from flask import current_app
from .http import get_json, post_json


def get_coniiti_data():
    return get_json(
        f"{current_app.config['INTEGRATIONS_SERVICE_URL']}/api/integrations/coniiti"
    )


def get_outlook_login_url(redirect_uri):
    return get_json(
        f"{current_app.config['INTEGRATIONS_SERVICE_URL']}/api/integrations/outlook/login-url",
        {"redirect_uri": redirect_uri},
    )


def exchange_outlook_code(code, redirect_uri):
    return post_json(
        f"{current_app.config['INTEGRATIONS_SERVICE_URL']}/api/integrations/outlook/exchange-code",
        {"code": code, "redirect_uri": redirect_uri},
    )
