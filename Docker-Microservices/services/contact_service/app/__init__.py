from flask import Flask
from .config import Config
from .repository import ContactRepository
from .routes import contact_bp
from .service import ContactService


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.contact_service = ContactService(ContactRepository(app.config["CONTACT_CSV_PATH"]))
    app.register_blueprint(contact_bp)

    @app.get('/health')
    def health():
        return {"status": "ok", "service": "contact_service"}

    return app
