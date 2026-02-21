from flask import Blueprint, render_template

from models.database import get_db

bp = Blueprint("principal", __name__, url_prefix="/principal")


@bp.route("/dashboard")
def dashboard():
    db = get_db()
    counts = {
        "students": db.execute("SELECT COUNT(*) c FROM students").fetchone()["c"],
        "subjects": db.execute("SELECT COUNT(*) c FROM subjects").fetchone()["c"],
        "exams": db.execute("SELECT COUNT(*) c FROM exams").fetchone()["c"],
    }
    return render_template("principal_dashboard.html", counts=counts)
