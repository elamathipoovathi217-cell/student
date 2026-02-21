from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.database import get_db
from utils.analytics import get_student_risk

bp = Blueprint("student", __name__, url_prefix="/student")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        reg_no = request.form.get("registration_no")
        dept = request.form.get("department")
        password = request.form.get("password")
        db = get_db()
        student = db.execute(
            "SELECT registration_no FROM students WHERE registration_no=? AND department=? AND password=?",
            (reg_no, dept, password),
        ).fetchone()
        if student:
            return redirect(url_for("student.profile", registration_no=reg_no))
        flash("Invalid student credentials", "danger")
    return render_template("student_login.html")


@bp.route("/<registration_no>")
def profile(registration_no):
    db = get_db()
    student = db.execute("SELECT * FROM students WHERE registration_no=?", (registration_no,)).fetchone()
    if not student:
        flash("Student not found", "danger")
        return redirect(url_for("student.login"))

    risk = get_student_risk(registration_no)
    return render_template("student_profile.html", student=student, risk=risk)
