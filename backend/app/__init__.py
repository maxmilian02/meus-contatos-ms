from flask import Flask
from app.auth import auth_bp
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "devkey")

    # Registro do Blueprint
    app.register_blueprint(auth_bp)

    return app
