from .coordinator import bp as coordinator_bp
from .hod import bp as hod_bp
from .principal import bp as principal_bp
from .public import bp as public_bp
from .student import bp as student_bp
from .teacher import bp as teacher_bp


def register_blueprints(app):
    app.register_blueprint(public_bp)
    app.register_blueprint(coordinator_bp)
    app.register_blueprint(hod_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(principal_bp)
