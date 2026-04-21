from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    jsonify,
    session,
    flash,
)
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import csv
import requests
from bs4 import BeautifulSoup
import math
import msal
import os

app = Flask(__name__)
app.secret_key = "secretkey123"

# -------------------- FLASK LOGIN --------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# -------------------- SCRAPING --------------------

def obtener_datos_coniiti():
    url = "https://coniiti.com/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "es-ES,es;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        titulos = [
            h.get_text(strip=True)
            for h in soup.find_all(["h1", "h2"])
            if h.get_text(strip=True)
        ]

        parrafos = [
            p.get_text(strip=True)
            for p in soup.find_all("p")
            if p.get_text(strip=True)
        ]

        return {
            "titulos": titulos[:5],
            "parrafos": parrafos[:5],
            "status": "ok",
        }

    except requests.exceptions.RequestException as e:
        return {"error": "No se pudo conectar", "detalle": str(e)}

# -------------------- API --------------------

@app.route("/api/coniiti")
@login_required
def api_coniiti():
    return jsonify(obtener_datos_coniiti())


@app.route("/coniiti")
@login_required
def ver_coniiti():
    datos = obtener_datos_coniiti()
    return render_template("coniiti.html", datos=datos)

# -------------------- USERS --------------------

def load_users():
    users = []
    try:
        with open("users.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                users.append(row)
    except FileNotFoundError:
        pass
    return users


user_list = load_users()


class User(UserMixin):
    def __init__(self, email):
        self.id = email


@login_manager.user_loader
def load_user(user_id):
    for u in user_list:
        if u["email"] == user_id:
            return User(user_id)
    return None

# -------------------- AUTH --------------------

@app.route("/")
def index():
    return render_template("inicio.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        for u in user_list:
            if u["email"] == email and u["password"] == password:
                login_user(User(email))
                return redirect(url_for("inicio"))

        error = "Credenciales incorrectas"

    return render_template("login.html", error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("inicio"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        user_list.append({"email": email, "password": password, "name": name})

        file_exists = os.path.isfile("users.csv")

        with open("users.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["email", "password", "name"])

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "email": email,
                "password": password,
                "name": name
            })

        return redirect(url_for("login"))

    return render_template("register.html")

# -------------------- ROUTES --------------------

@app.route("/inicio")
def inicio():
    return render_template("inicio.html")


@app.route("/pagina1")
@login_required
def pagina1():
    return render_template("pagina1.html")


@app.route("/pagina2")
@login_required
def pagina2():
    return render_template("pagina2.html")


@app.route("/memoria1")
@login_required
def memoria1():
    return render_template("memoria1.html")


@app.route("/memoria2")
@login_required
def memoria2():
    return render_template("memoria2.html")


@app.route("/acerca")
def acerca():
    return render_template("acerca.html")

# -------------------- CONTACTO --------------------

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        asunto = request.form["asunto"]
        mensaje = request.form.get("mensaje", "")

        archivo = "infopagweb.csv"
        existe = os.path.isfile(archivo)

        with open(archivo, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not existe:
                writer.writerow(["Nombre", "Correo", "Asunto", "Mensaje"])

            writer.writerow([nombre, correo, asunto, mensaje])

        flash("Mensaje enviado correctamente ✅")
        return redirect(url_for("contacto"))

    return render_template("contacto.html")

# -------------------- AGENDA --------------------

@app.route("/agenda")
def agenda():
    PONENTES = [
        {"nombre": "Dra. Martínez", "pais": "México"},
        {"nombre": "Ing. Pérez", "pais": "Colombia"},
    ]

    return render_template("agenda.html", ponentes=PONENTES)

# -------------------- MAIN --------------------

if __name__ == "__main__":
    app.run(debug=True)