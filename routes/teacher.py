from flask import Blueprint, render_template

from utils.analytics import teacher_student_analysis, teacher_subject_analysis

bp = Blueprint("teacher", __name__, url_prefix="/teacher")


@bp.route("/dashboard")
def dashboard():
    return render_template(
        "teacher_dashboard.html",
        subject_analysis=teacher_subject_analysis(),
        student_analysis=teacher_student_analysis(),
    )
