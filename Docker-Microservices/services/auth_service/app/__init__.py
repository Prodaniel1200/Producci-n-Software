from flask import Flask
from .config import Config
from .repository import UserRepository
from .routes import auth_bp
from .service import AuthService


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    repository = UserRepository(app.config["USERS_CSV_PATH"])
    app.auth_service = AuthService(repository)
    app.register_blueprint(auth_bp)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "auth_service"}

    return app
