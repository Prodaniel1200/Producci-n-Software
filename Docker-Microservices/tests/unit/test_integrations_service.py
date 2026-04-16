import pytest
from requests.exceptions import RequestException

from tests.conftest import service_import_path


class DummyResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        return None


@pytest.mark.unit
def test_coniiti_provider_extracts_titles_and_paragraphs(monkeypatch):
    html = """
    <html><body>
      <h1>CONIITI 2026</h1>
      <h2>Agenda principal</h2>
      <p>Primer parrafo.</p>
      <p>Segundo parrafo.</p>
    </body></html>
    """
    with service_import_path("integrations_service"):
        from app.providers import coniiti_provider

        monkeypatch.setattr(
            coniiti_provider.requests, "get", lambda *a, **k: DummyResponse(html)
        )
        result = coniiti_provider.obtener_datos_coniiti()

    assert result["status"] == "ok"
    assert "CONIITI 2026" in result["titulos"]
    assert "Primer parrafo." in result["parrafos"]


@pytest.mark.unit
def test_coniiti_provider_handles_request_exception(monkeypatch):
    with service_import_path("integrations_service"):
        from app.providers import coniiti_provider

        def boom(*args, **kwargs):
            raise RequestException("fallo")

        monkeypatch.setattr(coniiti_provider.requests, "get", boom)
        result = coniiti_provider.obtener_datos_coniiti()

    assert "error" in result


@pytest.mark.unit
def test_outlook_login_url_requires_configuration(integrations_client):
    response = integrations_client.get("/api/integrations/outlook/login-url")
    assert response.status_code == 400
    assert response.get_json()["ok"] is False


@pytest.mark.unit
def test_outlook_exchange_requires_code_and_redirect(integrations_client):
    response = integrations_client.post(
        "/api/integrations/outlook/exchange-code", json={}
    )
    assert response.status_code == 400
    assert response.get_json()["ok"] is False
