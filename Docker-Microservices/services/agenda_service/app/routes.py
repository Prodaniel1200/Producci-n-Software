from flask import Blueprint, jsonify, request
from .service import get_agenda


agenda_bp = Blueprint("agenda_api", __name__)


@agenda_bp.get("/api/agenda")
def agenda():
    return jsonify(get_agenda(page=request.args.get("page", 1, type=int), per_page=request.args.get("per_page", 5, type=int)))
