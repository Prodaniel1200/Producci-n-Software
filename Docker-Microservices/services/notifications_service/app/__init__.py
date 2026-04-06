from flask import Flask
from .routes import notifications_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(notifications_bp)

    @app.get('/health')
    def health():
        return {"status": "ok", "service": "notifications_service"}

    return app
