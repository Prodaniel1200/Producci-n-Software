import importlib.util
import os
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def service_import_path(service_name: str):
    service_dir = ROOT / "services" / service_name
    original = list(sys.path)
    to_clear_before = [name for name in sys.modules if name == "app" or name.startswith("app.")]
    for name in to_clear_before:
        sys.modules.pop(name, None)
    sys.path.insert(0, str(service_dir))
    try:
        yield service_dir
    finally:
        sys.path[:] = original
        to_clear_after = [name for name in sys.modules if name == "app" or name.startswith("app.")]
        for name in to_clear_after:
            sys.modules.pop(name, None)


def load_run_module(service_name: str):
    with service_import_path(service_name) as service_dir:
        run_path = service_dir / "run.py"
        module_name = f"{service_name}_run"
        spec = importlib.util.spec_from_file_location(module_name, run_path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module


@pytest.fixture
def auth_app(tmp_path, monkeypatch):
    users_csv = tmp_path / "users.csv"
    monkeypatch.setenv("USERS_CSV_PATH", str(users_csv))
    module = load_run_module("auth_service")
    module.app.config.update(TESTING=True)
    return module.app


@pytest.fixture
def auth_client(auth_app):
    with auth_app.test_client() as client:
        yield client


@pytest.fixture
def contact_app(tmp_path, monkeypatch):
    contact_csv = tmp_path / "contact_messages.csv"
    monkeypatch.setenv("CONTACT_CSV_PATH", str(contact_csv))
    module = load_run_module("contact_service")
    module.app.config.update(TESTING=True)
    return module.app


@pytest.fixture
def contact_client(contact_app):
    with contact_app.test_client() as client:
        yield client


@pytest.fixture
def agenda_app(monkeypatch):
    monkeypatch.setenv("NOTIFICATIONS_SERVICE_URL", "http://notifications-service:5000")
    monkeypatch.setenv("REQUEST_TIMEOUT", "1")
    module = load_run_module("agenda_service")
    module.app.config.update(TESTING=True)
    return module.app


@pytest.fixture
def agenda_client(agenda_app):
    with agenda_app.test_client() as client:
        yield client


@pytest.fixture
def integrations_app(monkeypatch):
    module = load_run_module("integrations_service")
    module.app.config.update(TESTING=True)
    return module.app


@pytest.fixture
def integrations_client(integrations_app):
    with integrations_app.test_client() as client:
        yield client


@pytest.fixture
def notifications_app():
    module = load_run_module("notifications_service")
    module.app.config.update(TESTING=True)
    return module.app


@pytest.fixture
def notifications_client(notifications_app):
    with notifications_app.test_client() as client:
        yield client


@pytest.fixture
def web_app(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("AUTH_SERVICE_URL", "http://auth-service:5000")
    monkeypatch.setenv("AGENDA_SERVICE_URL", "http://agenda-service:5000")
    monkeypatch.setenv("CONTACT_SERVICE_URL", "http://contact-service:5000")
    monkeypatch.setenv("INTEGRATIONS_SERVICE_URL", "http://integrations-service:5000")
    module = load_run_module("web_service")
    module.app.config.update(TESTING=True, SECRET_KEY="test-secret")
    return module.app


@pytest.fixture
def web_client(web_app):
    with web_app.test_client() as client:
        yield client


def login_web_user(web_client, email="test@example.com", name="Tester"):
    with web_client.session_transaction() as session:
        session["_user_id"] = email
        session["_fresh"] = True
        session["user_name"] = name
