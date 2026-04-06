import csv

import pytest

from tests.conftest import service_import_path


@pytest.mark.unit
def test_contact_service_requires_nombre_correo_y_asunto(tmp_path):
    with service_import_path("contact_service"):
        from app.repository import ContactRepository
        from app.service import ContactService

        service = ContactService(ContactRepository(str(tmp_path / "contact.csv")))
        result = service.create("", "correo@example.com", "Asunto", "Mensaje")

    assert result["ok"] is False
    assert "obligatorios" in result["error"]


@pytest.mark.unit
def test_contact_repository_writes_header_and_row(tmp_path):
    contact_csv = tmp_path / "contact.csv"
    with service_import_path("contact_service"):
        from app.repository import ContactRepository

        repo = ContactRepository(str(contact_csv))
        repo.save("Ana", "ana@example.com", "Consulta", "Hola")

    rows = list(csv.reader(contact_csv.open(encoding="utf-8")))
    assert rows[0] == ["Nombre", "Correo", "Asunto", "Mensaje"]
    assert rows[1] == ["Ana", "ana@example.com", "Consulta", "Hola"]


@pytest.mark.unit
def test_contact_route_returns_201_when_message_is_valid(contact_client):
    response = contact_client.post(
        "/api/contact",
        json={"nombre": "Ana", "correo": "ana@example.com", "asunto": "Consulta", "mensaje": "Hola"},
    )
    assert response.status_code == 201
    assert response.get_json()["ok"] is True


@pytest.mark.unit
def test_contact_route_returns_400_when_required_fields_are_missing(contact_client):
    response = contact_client.post(
        "/api/contact",
        json={"nombre": "", "correo": "ana@example.com", "asunto": "Consulta", "mensaje": "Hola"},
    )
    assert response.status_code == 400
    assert response.get_json()["ok"] is False
