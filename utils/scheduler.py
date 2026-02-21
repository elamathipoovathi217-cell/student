from datetime import datetime, timedelta

from models.database import get_db

SESSIONS = {
    "10am": ["10:00 AM"],
    "2pm": ["02:00 PM"],
    "both": ["10:00 AM", "02:00 PM"],
}


def _date_range(start, end):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


def generate_exam_schedule(start_date: str, end_date: str, session_mode: str):
    db = get_db()
    db.execute("DELETE FROM exams")

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    slots = []
    for day in _date_range(start, end):
        for t in SESSIONS.get(session_mode, SESSIONS["both"]):
            slots.append((day.isoformat(), t))

    subjects = db.execute(
        """
        SELECT s.id, s.department_id, s.year
        FROM subjects s
        ORDER BY s.year, s.department_id, s.id
        """
    ).fetchall()

    if len(slots) < len(subjects):
        raise ValueError("Date range does not have enough slots for all exams.")

    # Lightweight ML-like scoring: spread each department/year pair across different days.
    used_day_by_group = {}
    idx = 0
    for subject in subjects:
        group_key = (subject["department_id"], subject["year"])
        while idx < len(slots):
            day, time = slots[idx]
            if used_day_by_group.get(group_key) != day:
                db.execute(
                    "INSERT INTO exams(subject_id, exam_date, exam_time) VALUES (?,?,?)",
                    (subject["id"], day, time),
                )
                used_day_by_group[group_key] = day
                idx += 1
                break
            idx += 1

    db.commit()
    db.close()


def manual_schedule_entry(exam_date: str, exam_time: str, department_id: int, year: int, subject_id: int):
    db = get_db()
    subject = db.execute(
        "SELECT id FROM subjects WHERE id=? AND department_id=? AND year=?",
        (subject_id, department_id, year),
    ).fetchone()
    if not subject:
        raise ValueError("Chosen subject does not match department/year")

    db.execute(
        "INSERT INTO exams(subject_id, exam_date, exam_time) VALUES (?,?,?)",
        (subject_id, exam_date, exam_time),
    )
    db.commit()
    db.close()
