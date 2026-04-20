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
app.secret_key = os.environ.get("SECRET_KEY", "secretkey123")

# -------------------- FLASK LOGIN --------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# -------------------- HEALTH CHECK (AZURE) --------------------

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# -------------------- SCRAPING --------------------

def obtener_datos_coniiti():
    url = "https://coniiti.com/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        titulos = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2"])]
        parrafos = [p.get_text(strip=True) for p in soup.find_all("p")]

        return {"titulos": titulos[:5], "parrafos": parrafos[:5], "status": "ok"}

    except Exception as e:
        return {"error": str(e)}

# -------------------- LOGIN --------------------

def load_users():
    users = []
    try:
        with open("users.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            users = list(reader)
    except:
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

# -------------------- ROUTES --------------------

@app.route("/")
def index():
    return render_template("inicio.html")

@app.route("/inicio")
def inicio():
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

        with open("users.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["email", "password", "name"])
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow({"email": email, "password": password, "name": name})

        return redirect(url_for("login"))

    return render_template("register.html")

# -------------------- CONTACTO --------------------

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        archivo = "infopagweb.csv"

        with open(archivo, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                request.form["nombre"],
                request.form["correo"],
                request.form["asunto"],
                request.form.get("mensaje", "")
            ])

        flash("Mensaje enviado")
        return redirect(url_for("contacto"))

    return render_template("contacto.html")

# -------------------- OUTLOOK (FIX CRÍTICO) --------------------

CLIENT_ID = "TU_CLIENT_ID"
CLIENT_SECRET = "TU_SECRET_VALOR"
TENANT_ID = "TU_TENANT_ID"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read"]

def get_msal_app():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

@app.route("/login-outlook")
def login_outlook():
    auth_url = get_msal_app().get_authorization_request_url(
        SCOPE,
        redirect_uri=url_for("callback", _external=True)
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")

    result = get_msal_app().acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=url_for("callback", _external=True)
    )

    session["ms_token"] = result.get("access_token")
    return redirect(url_for("inicio"))

# -------------------- MAIN --------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)