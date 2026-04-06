from werkzeug.security import check_password_hash, generate_password_hash


class AuthService:
    def __init__(self, repository):
        self.repository = repository

    def register(self, name: str, email: str, password: str):
        if self.repository.get_by_email(email):
            return {"ok": False, "error": "El correo ya está registrado"}
        self.repository.create({"name": name, "email": email, "password": generate_password_hash(password)})
        return {"ok": True}

    def login(self, email: str, password: str):
        user = self.repository.get_by_email(email)
        if not user:
            return {"ok": False, "error": "Correo o contraseña incorrectos"}
        stored = user.get("password", "")
        if stored.startswith("scrypt:") or stored.startswith("pbkdf2:"):
            valid = check_password_hash(stored, password)
        else:
            valid = stored == password
        if not valid:
            return {"ok": False, "error": "Correo o contraseña incorrectos"}
        return {"ok": True, "user": {"email": user["email"], "name": user.get("name")}}
