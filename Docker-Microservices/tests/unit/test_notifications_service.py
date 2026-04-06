import pytest


@pytest.mark.unit
def test_notifications_health_endpoint(notifications_client):
    response = notifications_client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["service"] == "notifications_service"


@pytest.mark.unit
def test_notifications_endpoint_accepts_event(notifications_client):
    response = notifications_client.post(
        "/api/notifications/ponencia-created",
        json={"titulo": "IA Responsable", "ponente_nombre": "Ana", "fecha": "2026-05-10", "hora": "10:00"},
    )
    assert response.status_code == 202
    assert response.get_json()["ok"] is True


@pytest.mark.unit
def test_notifications_endpoint_validates_required_fields(notifications_client):
    response = notifications_client.post("/api/notifications/ponencia-created", json={"titulo": ""})
    assert response.status_code == 400
    assert response.get_json()["ok"] is False
