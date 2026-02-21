from flask import Flask

from models.database import init_db
from routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.secret_key = "student-performance-secret"

    @app.before_request
    def boot_db():
        init_db()

    register_blueprints(app)
    return app


app = create_app()


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
