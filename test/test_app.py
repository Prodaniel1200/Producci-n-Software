import pytest
import main.app as app_module

from requests.exceptions import RequestException


@pytest.fixture()
def client(monkeypatch):
    app_module.app.config.update(TESTING=True, SECRET_KEY="test-secret")

    monkeypatch.setattr(
        app_module,
        "render_template",
        lambda template_name, **context: f"{template_name}|{context}",
    )

    with app_module.app.test_client() as client:
        yield client


def login_as_test_user(client, monkeypatch):
    monkeypatch.setattr(
        app_module,
        "user_list",
        [{"email": "test@example.com", "password": "1234", "name": "Tester"}],
    )

    with client.session_transaction() as session:
        session["_user_id"] = "test@example.com"
        session["_fresh"] = True


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_api_coniiti_requires_login(client):
    response = client.get("/api/coniiti")
    assert response.status_code == 302


def test_api_coniiti_logged_in(client, monkeypatch):
    login_as_test_user(client, monkeypatch)

    monkeypatch.setattr(
        app_module,
        "obtener_datos_coniiti",
        lambda: {"status": "ok", "titulos": ["A"], "parrafos": ["B"]},
    )

    response = client.get("/api/coniiti")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_obtener_datos_coniiti_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise RequestException("fallo de conexion")

    monkeypatch.setattr(app_module.requests, "get", fake_get)

    result = app_module.obtener_datos_coniiti()

    assert result["error"] == "No se pudo conectar con el sitio"
