import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "student_performance.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db()
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_id INTEGER NOT NULL,
            year INTEGER NOT NULL,
            name TEXT NOT NULL,
            assigned_teacher TEXT,
            FOREIGN KEY(department_id) REFERENCES departments(id)
        );

        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            exam_date TEXT NOT NULL,
            exam_time TEXT NOT NULL,
            room_no TEXT,
            invigilator TEXT,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        );

        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_no TEXT UNIQUE NOT NULL,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            attendance REAL DEFAULT 0,
            internal1 REAL DEFAULT 0,
            internal2 REAL DEFAULT 0,
            seminar REAL DEFAULT 0,
            assessment REAL DEFAULT 0,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            posted_on TEXT NOT NULL
        );
        """
    )

    dept_count = cur.execute("SELECT COUNT(*) AS c FROM departments").fetchone()["c"]
    if dept_count == 0:
        departments = [
            "Computer Science",
            "Information Technology",
            "Electronics",
            "Mechanical",
            "Civil",
            "Electrical",
            "AI & Data Science",
        ]
        cur.executemany("INSERT INTO departments(name) VALUES(?)", [(d,) for d in departments])

    subject_count = cur.execute("SELECT COUNT(*) AS c FROM subjects").fetchone()["c"]
    if subject_count == 0:
        depts = cur.execute("SELECT id, name FROM departments ORDER BY id").fetchall()
        for dept in depts:
            for year in range(1, 5):
                for i in range(1, 6):
                    cur.execute(
                        "INSERT INTO subjects(department_id, year, name) VALUES(?,?,?)",
                        (dept["id"], year, f"{dept['name']} Subject {year}.{i}"),
                    )

    student_count = cur.execute("SELECT COUNT(*) AS c FROM students").fetchone()["c"]
    if student_count == 0:
        cur.executemany(
            """
            INSERT INTO students(registration_no, student_id, name, department, attendance, internal1, internal2, seminar, assessment, password)
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            [
                ("REG001", "S001", "Arun Kumar", "Computer Science", 82, 16, 17, 15, 16, "pass123"),
                ("REG002", "S002", "Meena R", "Information Technology", 68, 10, 11, 12, 10, "pass123"),
                ("REG003", "S003", "Rahul M", "AI & Data Science", 74, 13, 12, 14, 13, "pass123"),
            ],
        )

    notif_count = cur.execute("SELECT COUNT(*) AS c FROM notifications").fetchone()["c"]
    if notif_count == 0:
        cur.executemany(
            "INSERT INTO notifications(message, posted_on) VALUES (?, date('now'))",
            [
                ("Parent-Teacher Meeting on Friday 3PM",),
                ("Internal Exam Timetable Released",),
                ("Internal Exam Result Announcement next Monday",),
            ],
        )

    conn.commit()
    conn.close()
