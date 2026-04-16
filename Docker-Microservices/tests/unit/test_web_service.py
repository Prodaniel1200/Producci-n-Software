import pytest
from requests.exceptions import RequestException

from tests.conftest import login_web_user


@pytest.mark.unit
def test_public_home_route_is_accessible(web_client):
    response = web_client.get("/")
    assert response.status_code == 200


@pytest.mark.unit
def test_cookies_route_requires_login(web_client):
    response = web_client.get("/cookies")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


@pytest.mark.unit
def test_login_route_succeeds_with_mocked_auth_client(web_app, web_client, monkeypatch):
    auth_client_obj = web_app.view_functions["auth.login"].__globals__["auth_client"]
    monkeypatch.setattr(
        auth_client_obj,
        "login",
        lambda e, p: {"ok": True, "user": {"email": e, "name": "Ana"}},
    )
    response = web_client.post(
        "/login",
        data={"email": "ana@example.com", "password": "12345"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/inicio")


@pytest.mark.unit
def test_login_route_handles_auth_service_failure(web_app, web_client, monkeypatch):
    auth_client_obj = web_app.view_functions["auth.login"].__globals__["auth_client"]

    def boom(*args, **kwargs):
        raise RequestException("auth down")

    monkeypatch.setattr(auth_client_obj, "login", boom)
    response = web_client.post(
        "/login", data={"email": "ana@example.com", "password": "12345"}
    )

    assert response.status_code == 200
    assert b"Servicio de autentic" in response.data


@pytest.mark.unit
def test_register_route_redirects_on_success(web_app, web_client, monkeypatch):
    auth_client_obj = web_app.view_functions["auth.register"].__globals__["auth_client"]
    monkeypatch.setattr(auth_client_obj, "register", lambda n, e, p: {"ok": True})
    response = web_client.post(
        "/register",
        data={"name": "Ana", "email": "ana@example.com", "password": "12345"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


@pytest.mark.unit
def test_agenda_view_renders_fallback_when_service_is_down(
    web_app, web_client, monkeypatch
):
    agenda_client_obj = web_app.view_functions["agenda.view_agenda"].__globals__[
        "agenda_client"
    ]
    monkeypatch.setattr(
        agenda_client_obj,
        "get_agenda",
        lambda *a, **k: (_ for _ in ()).throw(RequestException("down")),
    )
    response = web_client.get("/agenda")

    assert response.status_code == 200


@pytest.mark.unit
def test_contact_view_flashes_success_after_submission(
    web_app, web_client, monkeypatch
):
    contact_client_obj = web_app.view_functions["contact.contacto"].__globals__[
        "contact_client"
    ]
    monkeypatch.setattr(
        contact_client_obj, "send_contact_message", lambda *a, **k: {"ok": True}
    )
    response = web_client.post(
        "/contacto",
        data={
            "nombre": "Ana",
            "correo": "ana@example.com",
            "asunto": "Consulta",
            "mensaje": "Hola",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Mensaje enviado correctamente" in response.data


@pytest.mark.unit
def test_coniiti_api_requires_login(web_client):
    response = web_client.get("/api/coniiti")
    assert response.status_code == 302


@pytest.mark.unit
def test_coniiti_api_returns_503_if_integrations_service_fails(
    web_app, web_client, monkeypatch
):
    login_web_user(web_client)
    monkeypatch.setitem(
        web_app.view_functions["integrations.api_coniiti"].__wrapped__.__globals__,
        "integrations_client",
        type(
            "IC",
            (),
            {
                "get_coniiti_data": staticmethod(
                    lambda: (_ for _ in ()).throw(RequestException("down"))
                )
            },
        )(),
    )
    response = web_client.get("/api/coniiti")

    assert response.status_code == 503


@pytest.mark.unit
def test_create_ponencia_view_survives_when_notifications_are_down(
    web_app, web_client, monkeypatch
):
    login_web_user(web_client)
    monkeypatch.setitem(
        web_app.view_functions["agenda.create_ponencia_view"].__wrapped__.__globals__,
        "agenda_client",
        type(
            "AC",
            (),
            {
                "create_ponencia": staticmethod(
                    lambda payload: {
                        "ok": True,
                        "notification_status": "degraded",
                        "warning": "La ponencia fue creada, pero el servicio de notificaciones no esta disponible",
                    }
                ),
                "get_agenda": staticmethod(
                    lambda page=1: {
                        "eventos": [],
                        "ponentes": [],
                        "page": 1,
                        "total_pages": 1,
                    }
                ),
            },
        )(),
    )
    response = web_client.post(
        "/ponentes/nueva",
        data={
            "nombre": "Ana",
            "pais": "Colombia",
            "titulo": "IA Responsable",
            "fecha": "2026-05-10",
            "hora": "10:00",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"notificaciones" in response.data


@pytest.mark.unit
def test_login_outlook_redirects_home_when_service_returns_error(
    web_app, web_client, monkeypatch
):
    integrations_client_obj = web_app.view_functions[
        "integrations.login_outlook"
    ].__globals__["integrations_client"]
    monkeypatch.setattr(
        integrations_client_obj,
        "get_outlook_login_url",
        lambda redirect_uri: {"ok": False},
    )
    response = web_client.get("/login-outlook")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/inicio")
