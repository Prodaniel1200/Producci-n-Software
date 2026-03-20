import pytest
import sys
import os

# 🔥 FORZAMOS LA RUTA A main
sys.path.append(os.path.abspath("main"))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_inicio_carga(client):
    response = client.get("/")
    assert response.status_code == 200


def test_boton_registro_existe(client):
    response = client.get("/")
    html = response.data.decode("utf-8")

    assert "Inscribirme" in html or "Registrarse" in html


def test_boton_registro_tiene_texto(client):
    response = client.get("/")
    html = response.data.decode("utf-8")

    assert "<a" in html
    assert "Inscribirme" in html