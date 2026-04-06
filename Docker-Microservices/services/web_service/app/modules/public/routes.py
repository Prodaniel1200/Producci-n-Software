from flask import Blueprint, render_template
from flask_login import login_required


public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    return render_template("inicio.html")


@public_bp.route("/inicio")
def inicio():
    return render_template("inicio.html")


@public_bp.route("/acerca")
def acerca():
    return render_template("acerca.html")


@public_bp.route("/cookies")
@login_required
def cookies():
    return render_template("cookies.html")


@public_bp.route("/referencias")
@login_required
def referencias():
    return render_template("referencias.html")


@public_bp.route("/pagina1")
@login_required
def pagina1():
    return render_template("pagina1.html", titulo="Página 1", mensaje="Espacio listo para crecer como módulo independiente.")


@public_bp.route("/pagina2")
@login_required
def pagina2():
    return render_template("pagina2.html", titulo="Página 2", mensaje="Espacio listo para crecer como módulo independiente.")


@public_bp.route("/memoria1")
@login_required
def memoria1():
    return render_template("memoria1.html", titulo="Memoria 1", mensaje="Espacio listo para crecer como módulo independiente.")


@public_bp.route("/memoria2")
@login_required
def memoria2():
    return render_template("memoria2.html", titulo="Memoria 2", mensaje="Espacio listo para crecer como módulo independiente.")
