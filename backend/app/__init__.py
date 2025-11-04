from flask import Flask, jsonify
from flask_cors import CORS
from .auth import auth_bp
from .contacts import contacts_bp
from config import Config
import os # Importe o 'os'

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
    # ROTA DE DEBUG - Adicione este bloco
    @app.route("/debug/env")
    def debug_env():
        return jsonify({
            "MS_REDIRECT_URI_from_config": app.config.get("MS_REDIRECT_URI"),
            "FRONTEND_URL_from_config": app.config.get("FRONTEND_URL"),
            "SECRET_KEY_is_set": bool(app.config.get("SECRET_KEY")),
            "MS_CLIENT_ID_is_set": bool(app.config.get("MS_CLIENT_ID")),
        })
    
    return app