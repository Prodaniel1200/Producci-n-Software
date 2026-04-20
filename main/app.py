from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import csv, requests, math, msal, os
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)

app.secret_key = os.environ.get("SECRET_KEY", "secretkey123")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------------- HEALTH ----------------
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# ---------------- USERS ----------------
def load_users():
    if not os.path.exists("users.csv"):
        return []
    with open("users.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

user_list = load_users()

class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if any(u["email"] == user_id for u in user_list) else None

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("inicio.html")

@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        for u in user_list:
            if u["email"] == email and u["password"] == password:
                login_user(User(email))
                return redirect(url_for("inicio"))

        return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("inicio"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            "email": request.form["email"],
            "password": request.form["password"],
            "name": request.form["name"]
        }

        user_list.append(data)

        with open("users.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- CONTACT ----------------
@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        with open("infopagweb.csv", "a", newline="", encoding="utf-8") as f:
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
#-------------------------------------------
    @app.route("/")
def root():
    return "OK - SERVICE RUNNING"
#----------------------------------------
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# ---------------- MAIN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)