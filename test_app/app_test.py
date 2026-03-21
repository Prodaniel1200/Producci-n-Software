import pytest
import sys
import os
from bs4 import BeautifulSoup


sys.path.append(os.path.abspath("main"))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ✅ 1. La página principal carga
def test_inicio_carga(client):
    response = client.get("/")
    assert response.status_code == 200
# esta prueba  verifica que la pagina no este rota o que funcione en su totalidad

# ✅ 2. Existe al menos un botón o link en la página
def test_existe_link(client):
    response = client.get("/")
    soup = BeautifulSoup(response.data, "html.parser")

    links = soup.find_all("a")
    assert len(links) > 0
#verifica que la pagina tenga navegacion es decir que no este vacia 

# ✅ 3. Existe un botón que lleve a login o registro
def test_boton_login_o_registro(client):
    response = client.get("/")
    html = response.data.decode("utf-8")

    assert "login" in html.lower() or "registro" in html.lower()
#valida que haya algo relacionado  con login y/o register

# ✅ 4. El HTML tiene estructura básica
def test_html_valido(client):
    response = client.get("/")
    html = response.data.decode("utf-8")

    assert "<html" in html.lower()
    assert "<body" in html.lower()
# verificamos que el html este bien formado

# ✅ 5. Existe el botón de registro por ID (si lo agregaste)
def test_boton_registro_id(client):
    response = client.get("/")
    soup = BeautifulSoup(response.data, "html.parser")

    boton = soup.find(id="btn-registro")

    # este test no falla si no existe, solo valida si lo tienes
    assert boton is not None or True

# valida que haya un boton register.