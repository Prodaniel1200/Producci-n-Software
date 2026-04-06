import requests
from flask import current_app


def _safe_json(response):
    try:
        return response.json()
    except ValueError:
        response.raise_for_status()
        raise


def get_json(url, params=None):
    response = requests.get(url, params=params, timeout=current_app.config["REQUEST_TIMEOUT"])
    if response.status_code >= 500:
        response.raise_for_status()
    data = _safe_json(response)
    if response.status_code >= 400 and not isinstance(data, dict):
        response.raise_for_status()
    return data


def post_json(url, payload):
    response = requests.post(url, json=payload, timeout=current_app.config["REQUEST_TIMEOUT"])
    if response.status_code >= 500:
        response.raise_for_status()
    data = _safe_json(response)
    if response.status_code >= 400 and not isinstance(data, dict):
        response.raise_for_status()
    return data
