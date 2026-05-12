from flask import Blueprint, render_template
from flask_login import current_user, login_required


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.name or current_user.id)


@admin_bp.route("/dashboard-superuser")
@login_required
def dashboard_superuser():
    return render_template("dashboard_superuser.html")
