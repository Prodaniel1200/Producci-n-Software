from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .extensions import login_manager
from .modules.auth.routes import auth_bp, User
from .modules.public.routes import public_bp
from .modules.agenda.routes import agenda_bp
from .modules.contact.routes import contact_bp
from .modules.integrations.routes import integrations_bp
from .modules.admin.routes import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.from_session(user_id)

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(agenda_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(integrations_bp)
    app.register_blueprint(admin_bp)

    @app.get('/health')
    def health():
        return {"status": "ok", "service": "web_service"}

    return app
