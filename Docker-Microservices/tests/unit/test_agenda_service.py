from copy import deepcopy

import pytest
from requests.exceptions import RequestException

from tests.conftest import service_import_path


@pytest.fixture
def agenda_service_module():
    with service_import_path("agenda_service"):
        from app import service as service_module

        yield service_module


@pytest.fixture
def reset_ponentes(agenda_service_module, monkeypatch):
    original = deepcopy(agenda_service_module.PONENTES)
    monkeypatch.setattr(agenda_service_module, "PONENTES", deepcopy(original))
    return agenda_service_module


@pytest.mark.unit
def test_get_agenda_returns_paginated_data(reset_ponentes):
    result = reset_ponentes.get_agenda(page=1, per_page=3)
    assert result["page"] == 1
    assert result["total_pages"] >= 3
    assert len(result["ponentes"]) == 3
    assert len(result["eventos"]) == 3


@pytest.mark.unit
def test_create_ponencia_validates_required_fields(reset_ponentes):
    result = reset_ponentes.create_ponencia(
        {
            "nombre": "",
            "pais": "Colombia",
            "titulo": "X",
            "fecha": "2026-05-10",
            "hora": "10:00",
        }
    )
    assert result["ok"] is False
    assert "faltantes" in result["error"]


@pytest.mark.unit
def test_create_ponencia_succeeds_and_marks_notification_sent(reset_ponentes):
    result = reset_ponentes.create_ponencia(
        {
            "nombre": "Ana",
            "pais": "Colombia",
            "titulo": "IA Responsable",
            "fecha": "2026-05-10",
            "hora": "10:00",
        },
        notifier=lambda payload: {"ok": True, "message": payload["titulo"]},
    )
    assert result["ok"] is True
    assert result["notification_status"] == "sent"
    assert any(p["nombre"] == "Ana" for p in reset_ponentes.PONENTES)


@pytest.mark.unit
def test_create_ponencia_keeps_system_alive_when_notifications_fail(reset_ponentes):
    def failing_notifier(payload):
        raise RequestException("service down")

    result = reset_ponentes.create_ponencia(
        {
            "nombre": "Ana",
            "pais": "Colombia",
            "titulo": "IA Responsable",
            "fecha": "2026-05-10",
            "hora": "10:00",
        },
        notifier=failing_notifier,
    )
    assert result["ok"] is True
    assert result["notification_status"] == "degraded"
    assert "notificaciones" in result["warning"]


@pytest.mark.unit
def test_agenda_route_returns_json(agenda_client):
    response = agenda_client.get("/api/agenda?page=1&per_page=2")
    assert response.status_code == 200
    body = response.get_json()
    assert body["page"] == 1
    assert len(body["eventos"]) == 2


@pytest.mark.unit
def test_create_ponente_route_still_returns_201_when_notification_service_is_down(
    agenda_client, monkeypatch
):
    with service_import_path("agenda_service"):
        import app.routes as routes_module

        def boom(*args, **kwargs):
            raise RequestException("notifications unavailable")

        monkeypatch.setattr(routes_module.requests, "post", boom)
        response = agenda_client.post(
            "/api/ponentes",
            json={
                "nombre": "Ana",
                "pais": "Colombia",
                "titulo": "IA Responsable",
                "fecha": "2026-05-10",
                "hora": "10:00",
            },
        )

    assert response.status_code == 201
    assert response.get_json()["notification_status"] == "degraded"
