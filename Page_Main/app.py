from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random

app = Flask(__name__)
app.secret_key = "secretkey123"

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Lista de usuarios (simulación de DB)
user_list = [
    {"email": "nslopez90@ucatolica.edu.co", "password": "12345", "name": "Natalia López"},
    {"email": "jperez@example.com", "password": "12345", "name": "Juan Pérez"},
]

class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def load_user(user_id):
    for u in user_list:
        if u["email"] == user_id:
            return User(user_id)
    return None

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        for row in user_list:
            if row["email"] == email and row["password"] == password:
                user = User(email)
                login_user(user)
                return redirect(url_for("dashboard"))
        error = "Correo o contraseña incorrectos"
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        # Verificar si ya existe
        if any(u["email"] == email for u in user_list):
            error = "El correo ya está registrado"
        else:
            user_list.append({"email": email, "password": password, "name": name})
            return redirect(url_for("login"))
    return render_template("register.html", error=error)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.id)

@app.route("/agenda")
@login_required
def agenda():
    # Lista de ponentes con nacionalidad y bandera fija
    ponentes = [
        {"nombre": "Dra. Martínez", "pais": "México", "bandera": "https://s1.significados.com/foto/bandera-mexico.jpg?class=article"},
        {"nombre": "Ing. Pérez", "pais": "Colombia", "bandera": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Flag_of_Colombia.svg/960px-Flag_of_Colombia.svg.png"},
        {"nombre": "Dr. López", "pais": "Argentina", "bandera": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Flag_of_Argentina.svg/960px-Flag_of_Argentina.svg.png"},
        {"nombre": "Dra. González", "pais": "España", "bandera": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Flag_of_Spain.svg/960px-Flag_of_Spain.svg.png"},
        {"nombre": "Dr. Fernández", "pais": "Chile", "bandera": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Flag_of_Chile.svg/960px-Flag_of_Chile.svg.png"},
        {"nombre": "Ing. Martínez", "pais": "Perú", "bandera": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Flag_of_Peru_%28state%29.svg/960px-Flag_of_Peru_%28state%29.svg.png"},
    ]

    tipos_eventos = ["Conferencia", "Ponencia", "Taller"]
    titulos_eventos = ["Innovación tecnológica", "Nuevas tendencias en IA", "Salud digital", 
                       "Programación Python", "Blockchain en educación", "Ciberseguridad"]
    horas = ["09:00 - 09:45", "10:00 - 10:30", "10:45 - 11:15", "11:30 - 12:15", "12:30 - 13:15", "14:00 - 14:45"]

    eventos = []
    for i in range(len(horas)):
        ponente = random.choice(ponentes)  # Ponente fijo con su país y bandera
        evento = {
            "hora": horas[i],
            "tipo": random.choice(tipos_eventos),
            "titulo": random.choice(titulos_eventos),
            "ponente": ponente["nombre"],
            "pais": ponente["pais"],
            "bandera": ponente["bandera"]
        }
        eventos.append(evento)

    return render_template("agenda.html", calendario=eventos)

if __name__ == "__main__":
    app.run(debug=True)
