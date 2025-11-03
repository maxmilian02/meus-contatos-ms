from flask import Flask
from flask_cors import CORS
from .auth import auth_bp
from .contacts import contacts_bp
from config import Config

def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True)

    # register blueprints
    app.register_blueprint(auth_bp)        # routes under /auth/...
    app.register_blueprint(contacts_bp)    # routes under /contacts/...

    # simple healthcheck
    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app
