from flask import Blueprint, flash, redirect, render_template, request, url_for
from requests.exceptions import RequestException

from ...clients import contact_client


contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        try:
            result = contact_client.send_contact_message(request.form["nombre"], request.form["correo"], request.form["asunto"], request.form.get("mensaje", ""))
            if result.get("ok"):
                flash("Mensaje enviado correctamente ✅")
                return redirect(url_for("contact.contacto"))
            flash(result.get("error", "No se pudo enviar el mensaje"), "danger")
        except RequestException:
            flash("Servicio de contacto no disponible", "danger")
    return render_template("contacto.html")
