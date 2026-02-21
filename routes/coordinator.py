from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.database import get_db
from utils.scheduler import generate_exam_schedule, manual_schedule_entry

bp = Blueprint("coordinator", __name__, url_prefix="/coordinator")


@bp.route("/timetable", methods=["GET", "POST"])
def timetable_generator():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        session_mode = request.form.get("session_mode", "both")
        method = request.form.get("method", "ml")

        if method == "manual":
            try:
                manual_schedule_entry(
                    exam_date=request.form.get("manual_date"),
                    exam_time=request.form.get("manual_time"),
                    department_id=int(request.form.get("manual_department")),
                    year=int(request.form.get("manual_year")),
                    subject_id=int(request.form.get("manual_subject")),
                )
                flash("Manual exam allocation added.", "success")
            except Exception as exc:
                flash(f"Manual allocation failed: {exc}", "danger")
        else:
            try:
                generate_exam_schedule(start_date, end_date, session_mode)
                flash("Exam timetable generated using ML-based scheduler.", "success")
            except Exception as exc:
                flash(f"Unable to generate timetable: {exc}", "danger")

        return redirect(url_for("public.schedule_page"))

    db = get_db()
    departments = db.execute("SELECT id, name FROM departments ORDER BY name").fetchall()
    subjects = db.execute(
        "SELECT s.id, s.name, s.year, d.name as department FROM subjects s JOIN departments d ON s.department_id=d.id ORDER BY d.name, s.year, s.name"
    ).fetchall()
    return render_template("timetable.html", departments=departments, subjects=subjects)


@bp.route("/room-invigilator", methods=["GET", "POST"])
def room_invigilator():
    db = get_db()
    if request.method == "POST":
        exam_id = int(request.form.get("exam_id"))
        room_no = request.form.get("room_no")
        invigilator = request.form.get("invigilator")
        db.execute("UPDATE exams SET room_no=?, invigilator=? WHERE id=?", (room_no, invigilator, exam_id))
        db.commit()
        flash("Room and invigilator updated.", "success")
        return redirect(url_for("coordinator.room_invigilator"))

    exams = db.execute(
        """
        SELECT e.id, e.exam_date, e.exam_time, s.name AS subject, d.name AS department, s.year,
               IFNULL(e.room_no, '') AS room_no, IFNULL(e.invigilator, '') AS invigilator
        FROM exams e
        JOIN subjects s ON e.subject_id=s.id
        JOIN departments d ON s.department_id=d.id
        ORDER BY e.exam_date, e.exam_time
        """
    ).fetchall()
    return render_template("room_invigilator.html", exams=exams)
