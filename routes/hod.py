from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.database import get_db

bp = Blueprint("hod", __name__, url_prefix="/hod")


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    db = get_db()
    if request.method == "POST":
        subject_id = int(request.form.get("subject_id"))
        teacher_name = request.form.get("teacher_name")
        db.execute("UPDATE subjects SET assigned_teacher=? WHERE id=?", (teacher_name, subject_id))
        db.commit()
        flash("Teacher assigned by HOD.", "success")
        return redirect(url_for("hod.dashboard"))

    subjects = db.execute(
        "SELECT s.id, s.name, s.year, d.name AS department, IFNULL(s.assigned_teacher, 'Not Assigned') assigned_teacher FROM subjects s JOIN departments d ON d.id=s.department_id ORDER BY d.name, s.year"
    ).fetchall()
    return render_template("hod_dashboard.html", subjects=subjects)
