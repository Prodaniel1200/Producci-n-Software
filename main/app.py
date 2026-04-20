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
import msal
import os

app = Flask(__name__)

# 🔐 FIX Azure (clave dinámica)
app.secret_key = os.environ.get("SECRET_KEY", "secretkey123")

# -------------------- FLASK LOGIN --------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# -------------------- HEALTH CHECK (IMPORTANTE AZURE) --------------------

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

# -------------------- USUARIOS --------------------

def load_users():
    users = []
    try:
        if os.path.exists("users.csv"):
            with open("users.csv", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                users = list(reader)
    except Exception as e:
        print("Error cargando usuarios:", e)

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
    try:
        return render_template("inicio.html")
    except Exception as e:
        return f"Error cargando inicio.html: {e}", 500


@app.route("/inicio")
def inicio():
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        for u in user_list:
            if u["email"] == email and u["password"] == password:
                login_user(User(email))
                return redirect(url_for("index"))

        error = "Credenciales incorrectas"

    return render_template("login.html", error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        user_list.append({"email": email, "password": password, "name": name})

        try:
            with open("users.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["email", "password", "name"])

                if f.tell() == 0:
                    writer.writeheader()

                writer.writerow({"email": email, "password": password, "name": name})
        except Exception as e:
            return f"Error guardando usuario: {e}", 500

        return redirect(url_for("login"))

    return render_template("register.html")


# -------------------- CONTACTO --------------------

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        try:
            with open("infopagweb.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    request.form.get("nombre"),
                    request.form.get("correo"),
                    request.form.get("asunto"),
                    request.form.get("mensaje", "")
                ])
        except Exception as e:
            return f"Error guardando contacto: {e}", 500

        flash("Mensaje enviado")
        return redirect(url_for("contacto"))

    return render_template("contacto.html")


# -------------------- OUTLOOK --------------------

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
    return redirect(url_for("index"))

# -------------------- MAIN (CRÍTICO AZURE) --------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)