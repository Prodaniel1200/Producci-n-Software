import pytest
from werkzeug.security import check_password_hash

from tests.conftest import  service_import_path


@pytest.mark.unit
def test_register_hashes_password_and_persists_user(tmp_path):
    users_csv = tmp_path / "users.csv"
    with service_import_path("auth_service"):
        from app.repository import UserRepository
        from app.service import AuthService

        repo = UserRepository(str(users_csv))
        service = AuthService(repo)

        result = service.register("Ana", "ana@example.com", "12345")
        stored = repo.get_by_email("ana@example.com")

    assert result == {"ok": True}
    assert stored is not None
    assert stored["password"] != "12345"
    assert check_password_hash(stored["password"], "12345")


@pytest.mark.unit
def test_register_rejects_duplicate_email(tmp_path):
    users_csv = tmp_path / "users.csv"
    with service_import_path("auth_service"):
        from app.repository import UserRepository
        from app.service import AuthService

        repo = UserRepository(str(users_csv))
        service = AuthService(repo)
        service.register("Ana", "ana@example.com", "12345")
        result = service.register("Ana 2", "ana@example.com", "99999")

    assert result["ok"] is False
    assert "registrado" in result["error"]


@pytest.mark.unit
def test_login_accepts_legacy_plaintext_password(tmp_path):
    users_csv = tmp_path / "users.csv"
    users_csv.write_text("email,password,name\nlegacy@example.com,1234,Legacy\n", encoding="utf-8")
    with service_import_path("auth_service"):
        from app.repository import UserRepository
        from app.service import AuthService

        result = AuthService(UserRepository(str(users_csv))).login("legacy@example.com", "1234")

    assert result["ok"] is True
    assert result["user"]["email"] == "legacy@example.com"


@pytest.mark.unit
def test_login_rejects_invalid_password(tmp_path):
    users_csv = tmp_path / "users.csv"
    with service_import_path("auth_service"):
        from app.repository import UserRepository
        from app.service import AuthService

        repo = UserRepository(str(users_csv))
        service = AuthService(repo)
        service.register("Ana", "ana@example.com", "12345")
        result = service.login("ana@example.com", "wrong")

    assert result["ok"] is False
    assert "incorrectos" in result["error"]


@pytest.mark.unit
def test_auth_routes_register_and_login(auth_client):
    register_response = auth_client.post(
        "/api/auth/register",
        json={"name": "Ana", "email": "ana@example.com", "password": "12345"},
    )
    login_response = auth_client.post(
        "/api/auth/login",
        json={"email": "ana@example.com", "password": "12345"},
    )

    assert register_response.status_code == 201
    assert login_response.status_code == 200
    assert login_response.get_json()["user"]["name"] == "Ana"


@pytest.mark.unit
def test_auth_route_returns_401_for_bad_credentials(auth_client):
    response = auth_client.post("/api/auth/login", json={"email": "x@example.com", "password": "bad"})
    assert response.status_code == 401
    assert response.get_json()["ok"] is False
