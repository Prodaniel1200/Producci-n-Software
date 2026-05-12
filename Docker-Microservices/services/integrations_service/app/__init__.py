from flask import Flask
from .config import Config
from .routes import integrations_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(integrations_bp)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "integrations_service"}

    return app
