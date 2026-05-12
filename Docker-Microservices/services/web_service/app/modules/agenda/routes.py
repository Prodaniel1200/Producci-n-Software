from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from requests.exceptions import RequestException

from ...clients import agenda_client


agenda_bp = Blueprint("agenda", __name__)


@agenda_bp.route("/agenda")
def view_agenda():
    page = request.args.get("page", 1, type=int)
    try:
        data = agenda_client.get_agenda(page=page)
        return render_template(
            "agenda.html",
            eventos=data["eventos"],
            ponentes=data["ponentes"],
            page=data["page"],
            total_pages=data["total_pages"],
        )
    except RequestException:
        flash("Servicio de agenda no disponible", "danger")
        return render_template(
            "agenda.html", eventos=[], ponentes=[], page=1, total_pages=1
        )


@agenda_bp.route("/ponentes/nueva", methods=["GET", "POST"])
@login_required
def create_ponencia_view():
    if request.method == "POST":
        payload = {
            "nombre": request.form.get("nombre", ""),
            "pais": request.form.get("pais", ""),
            "bandera": request.form.get("bandera", "banderas/mexico.png"),
            "titulo": request.form.get("titulo", ""),
            "tipo": request.form.get("tipo", "Ponencia"),
            "fecha": request.form.get("fecha", ""),
            "hora": request.form.get("hora", ""),
            "modalidad": request.form.get("modalidad", "Presencial"),
            "sede": request.form.get("sede", "Claustro"),
            "salon": request.form.get("salon", "Auditorio Nuevo"),
        }
        try:
            result = agenda_client.create_ponencia(payload)
            if result.get("ok"):
                if result.get("notification_status") == "degraded":
                    flash(
                        result.get(
                            "warning",
                            "La ponencia fue creada, pero el servicio de notificaciones no respondio",
                        ),
                        "warning",
                    )
                else:
                    flash("Ponencia creada correctamente ✅", "success")
                return redirect(url_for("agenda.view_agenda"))
            flash(result.get("error", "No fue posible crear la ponencia"), "danger")
        except RequestException:
            flash("Servicio de agenda no disponible", "danger")
    return render_template("crear_ponencia.html")
