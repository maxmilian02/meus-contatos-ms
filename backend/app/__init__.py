from flask import Flask
from flask_cors import CORS
from .auth import auth_bp
from .contacts import contacts_bp
from config import Config

def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    
    # Validar configuração
    try:
        Config.validate()
    except ValueError as e:
        print(f"ERRO DE CONFIGURAÇÃO: {e}")
        raise
    
    # Configurar CORS com credenciais
    CORS(app, 
         supports_credentials=True,
         origins=[app.config["FRONTEND_URL"]],
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "OPTIONS"])
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(contacts_bp)
    
    # Healthcheck
    @app.route("/health")
    def health():
        return {
            "status": "ok",
            "config": {
                "client_id_set": bool(app.config.get("MS_CLIENT_ID")),
                "redirect_uri": app.config.get("MS_REDIRECT_URI")
            }
        }, 200

    return app