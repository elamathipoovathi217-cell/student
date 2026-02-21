from models.database import get_db


def _final_internal(mark_row):
    total = (
        mark_row["attendance"]
        + mark_row["internal1"]
        + mark_row["internal2"]
        + mark_row["seminar"]
        + mark_row["assessment"]
    )
    return round(total / 20.0, 2)


def get_student_risk(registration_no: str):
    db = get_db()
    s = db.execute("SELECT * FROM students WHERE registration_no=?", (registration_no,)).fetchone()
    db.close()
    score = _final_internal(s)

    if s["attendance"] < 70:
        status = "Critical"
    elif score < 0.75:
        status = "High Risk"
    elif score < 1.0:
        status = "Average"
    else:
        status = "Safe"

    return {
        "internal_score": round(score * 20, 2),
        "status": status,
        "improvement_needed": round(max(0, 15 - (score * 20)), 2),
    }


def teacher_subject_analysis():
    db = get_db()
    rows = db.execute(
        "SELECT department, AVG((internal1+internal2+seminar+assessment)/4.0) as avg_marks FROM students GROUP BY department"
    ).fetchall()
    db.close()
    return rows


def teacher_student_analysis():
    db = get_db()
    rows = db.execute(
        "SELECT registration_no, name, department, attendance, internal1, internal2 FROM students ORDER BY department, name"
    ).fetchall()
    db.close()
    return rows
