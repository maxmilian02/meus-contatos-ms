import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Chave secreta para sessões - IMPORTANTE: use uma chave forte
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24).hex())
    
    # Configurações do Microsoft OAuth2
    MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
    MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
    MS_AUTHORITY = os.getenv("MS_AUTHORITY", "https://login.microsoftonline.com/common")
    MS_REDIRECT_URI = os.getenv("MS_REDIRECT_URI", "http://localhost:5000/auth/login/callback")
    
    # URL do frontend
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Configurações de sessão
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False  # True em produção com HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_NAME = 'ms_contacts_session'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
    
    # Validação de configuração
    @staticmethod
    def validate():
        if not Config.MS_CLIENT_ID:
            raise ValueError("MS_CLIENT_ID não configurado no .env")
        if not Config.MS_CLIENT_SECRET:
            raise ValueError("MS_CLIENT_SECRET não configurado no .env")