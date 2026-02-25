from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import csv
import requests
from bs4 import BeautifulSoup
import math

app = Flask(__name__)
app.secret_key = "secretkey123"

# -------------------- FLASK LOGIN --------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# -------------------- FUNCION SCRAPING CONIITI --------------------

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

        titulos = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2"]) if h.get_text(strip=True)]
        parrafos = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]

        return {
            "titulos": titulos[:5],
            "parrafos": parrafos[:5],
            "status": "ok"
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": "No se pudo conectar con el sitio",
            "detalle": str(e)
        }

# -------------------- API ENDPOINT --------------------

@app.route("/api/coniiti")
@login_required
def api_coniiti():
    return jsonify(obtener_datos_coniiti())

@app.route("/coniiti")
@login_required
def ver_coniiti():
    datos = obtener_datos_coniiti()
    return render_template("coniiti.html", datos=datos)

# -------------------- CARGA USUARIOS --------------------

def load_users():
    users = []
    try:
        with open('users.csv', newline='', encoding='utf-8') as csvfile:
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

# -------------------- LOGIN / LOGOUT / REGISTER --------------------

@app.route("/")
def index():
    return redirect(url_for("inicio"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        for row in user_list:
            if row["email"] == email and row["password"] == password:
                login_user(User(email))
                return redirect(url_for("inicio"))

        error = "Correo o contraseña incorrectos"

    return render_template("login.html", error=error)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if any(u["email"] == email for u in user_list):
            error = "El correo ya está registrado"
        else:
            user_list.append({"email": email, "password": password, "name": name})

            with open('users.csv', 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['email', 'password', 'name']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow({"email": email, "password": password, "name": name})

            return redirect(url_for("login"))

    return render_template("register.html", error=error)

# -------------------- RUTAS PRINCIPALES --------------------

@app.route("/inicio")
@login_required
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

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

# -------------------- AGENDA CON PAGINACIÓN --------------------

@app.route("/agenda")
@login_required
def agenda():

    # -------- LISTA DE PONENTES --------
    PONENTES = [
        {"nombre": "Dra. Martínez", "pais": "México", "bandera": "banderas/mexico.png"},
        {"nombre": "Ing. Pérez", "pais": "Colombia", "bandera": "banderas/colombia.png"},
        {"nombre": "Dr. López", "pais": "Argentina", "bandera": "banderas/argentina.png"},
        {"nombre": "Dr. Hans Müller", "pais": "Alemania", "bandera": "banderas/alemania.png"},
        {"nombre": "Dr. Jean Dupont", "pais": "Francia", "bandera": "banderas/francia.png"},
        {"nombre": "Ing. Carlos Silva", "pais": "Brasil", "bandera": "banderas/brasil.png"},
        {"nombre": "Dra. Sofía Rodríguez", "pais": "Panamá", "bandera": "banderas/panama.png"},
        {"nombre": "Dr. Ana Torres", "pais": "México", "bandera": "banderas/mexico.png"},
        {"nombre": "Dr. Felipe Gómez", "pais": "Colombia", "bandera": "banderas/colombia.png"},
        {"nombre": "Dr. Laura Sánchez", "pais": "Argentina", "bandera": "banderas/argentina.png"},
        {"nombre": "Dr. Klaus Weber", "pais": "Alemania", "bandera": "banderas/alemania.png"},
        {"nombre": "Dr. Marie Dubois", "pais": "Francia", "bandera": "banderas/francia.png"},
        {"nombre": "Dr. Pedro Almeida", "pais": "Brasil", "bandera": "banderas/brasil.png"},
        {"nombre": "Dr. Ricardo Castillo", "pais": "Panamá", "bandera": "banderas/panama.png"},
    ]

    # -------- PAGINACIÓN --------
    page = request.args.get("page", 1, type=int)
    per_page = 5

    total = len(PONENTES)
    total_pages = math.ceil(total / per_page)

    start = (page - 1) * per_page
    end = start + per_page

    ponentes_paginados = PONENTES[start:end]

    # -------- EVENTOS --------
    eventos = [
        {
            "fecha": "2026-05-10",
            "hora": "09:00",
            "tipo": "Conferencia",
            "titulo": "Innovación tecnológica",
            "ponente": PONENTES[0],
            "modalidad": "Presencial",
            "sede": "Claustro",
            "salon": "Auditorio Principal"
        },
        {
            "fecha": "2026-05-10",
            "hora": "11:00",
            "tipo": "Ponencia",
            "titulo": "Nuevas tendencias en IA",
            "ponente": PONENTES[3],
            "modalidad": "Virtual",
            "sede": None,
            "salon": None
        },
        {
            "fecha": "2026-05-11",
            "hora": "08:30",
            "tipo": "Taller",
            "titulo": "Salud digital",
            "ponente": PONENTES[2],
            "modalidad": "Presencial",
            "sede": "Sede 4",
            "salon": "Salón 204"
        },
        {
            "fecha": "2026-05-11",
            "hora": "10:30",
            "tipo": "Conferencia",
            "titulo": "Transformación digital empresarial",
            "ponente": PONENTES[4],
            "modalidad": "Virtual",
            "sede": None,
            "salon": None
        }
    ]

    return render_template(
        "agenda.html",
        eventos=eventos,
        ponentes=ponentes_paginados,
        page=page,
        total_pages=total_pages
    )

# -------------------- MAIN --------------------

if __name__ == "__main__":
    app.run(debug=True)