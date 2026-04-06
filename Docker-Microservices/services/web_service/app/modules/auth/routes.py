from dataclasses import dataclass
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import UserMixin, login_required, login_user, logout_user
from requests.exceptions import RequestException

from ...clients import auth_client


auth_bp = Blueprint("auth", __name__)


@dataclass
class User(UserMixin):
    email: str
    name: str | None = None

    @property
    def id(self):
        return self.email

    @classmethod
    def from_session(cls, user_id):
        return cls(email=user_id, name=session.get("user_name"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        try:
            result = auth_client.login(request.form["email"], request.form["password"])
            if result.get("ok"):
                user = User(email=result["user"]["email"], name=result["user"].get("name"))
                session["user_name"] = user.name
                login_user(user)
                return redirect(url_for("public.inicio"))
            error = result.get("error", "No fue posible iniciar sesión")
        except RequestException:
            error = "Servicio de autenticación no disponible"
    return render_template("login.html", error=error)


@auth_bp.route("/logout")
@login_required
def logout():
    session.pop("user_name", None)
    session.pop("ms_token", None)
    logout_user()
    return redirect(url_for("public.inicio"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        try:
            result = auth_client.register(request.form["name"], request.form["email"], request.form["password"])
            if result.get("ok"):
                flash("Usuario registrado correctamente ✅")
                return redirect(url_for("auth.login"))
            error = result.get("error", "No fue posible registrar el usuario")
        except RequestException:
            error = "Servicio de autenticación no disponible"
    return render_template("register.html", error=error)
