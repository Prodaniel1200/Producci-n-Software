from flask import Blueprint, render_template, request
from requests.exceptions import RequestException

from ...clients import agenda_client


agenda_bp = Blueprint("agenda", __name__)


@agenda_bp.route("/agenda")
def view_agenda():
    page = request.args.get("page", 1, type=int)
    try:
        data = agenda_client.get_agenda(page=page)
        return render_template("agenda.html", eventos=data["eventos"], ponentes=data["ponentes"], page=data["page"], total_pages=data["total_pages"])
    except RequestException:
        return render_template("agenda.html", eventos=[], ponentes=[], page=1, total_pages=1)
