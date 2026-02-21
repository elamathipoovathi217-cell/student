# Student Performance Analysis System

A Flask + SQLite project with modular structure for coordinator-led timetable creation, room/invigilator assignment, HOD teacher assignment, student risk analysis, and public views.

## Project Structure

- `app.py` - application factory and blueprint registration
- `routes/` - module-wise route handlers
  - `public.py`
  - `coordinator.py`
  - `hod.py`
  - `teacher.py`
  - `student.py`
  - `principal.py`
- `models/database.py` - SQLite schema and seed data
- `utils/scheduler.py` - AI/ML-style auto timetable + manual allocation
- `utils/analytics.py` - risk analysis and dashboard analytics
- `templates/` - HTML views
- `static/` - CSS/JS assets

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

Default student login:
- REG001 / Computer Science / pass123
