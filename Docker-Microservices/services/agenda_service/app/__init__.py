from flask import Flask
from .routes import agenda_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(agenda_bp)

    @app.get('/health')
    def health():
        return {"status": "ok", "service": "agenda_service"}

    return app
