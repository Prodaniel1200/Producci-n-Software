from flask import current_app
from .http import post_json


def login(email, password):
    return post_json(f"{current_app.config['AUTH_SERVICE_URL']}/api/auth/login", {"email": email, "password": password})


def register(name, email, password):
    return post_json(f"{current_app.config['AUTH_SERVICE_URL']}/api/auth/register", {"name": name, "email": email, "password": password})
