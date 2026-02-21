from flask import Blueprint, render_template

from models.database import get_db

bp = Blueprint("public", __name__)


@bp.route("/")
def index():
    db = get_db()
    timetable = db.execute(
        """
        SELECT e.exam_date, e.exam_time, d.name AS department, s.year, s.name AS subject,
               IFNULL(e.room_no, 'TBD') AS room_no, IFNULL(e.invigilator, 'TBD') AS invigilator
        FROM exams e
        JOIN subjects s ON e.subject_id = s.id
        JOIN departments d ON s.department_id = d.id
        ORDER BY e.exam_date, e.exam_time
        """
    ).fetchall()
    notifications = db.execute("SELECT message, posted_on FROM notifications ORDER BY posted_on DESC").fetchall()
    return render_template("index.html", timetable=timetable, notifications=notifications)


@bp.route("/schedule.html")
def schedule_page():
    db = get_db()
    schedule = db.execute(
        """
        SELECT e.exam_date, e.exam_time, d.name AS department, s.year, s.name AS subject,
               IFNULL(e.room_no, 'Not Assigned') AS room_no,
               IFNULL(e.invigilator, 'Not Assigned') AS invigilator
        FROM exams e
        JOIN subjects s ON e.subject_id = s.id
        JOIN departments d ON s.department_id = d.id
        ORDER BY e.exam_date, e.exam_time, d.name
        """
    ).fetchall()
    return render_template("schedule.html", schedule=schedule)
