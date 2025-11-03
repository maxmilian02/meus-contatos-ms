import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "devkey")
    MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
    MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
    MS_AUTHORITY = os.getenv("MS_AUTHORITY", "https://login.microsoftonline.com/common")
    MS_REDIRECT_URI = os.getenv("MS_REDIRECT_URI", "http://localhost:5000/auth/login/callback")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
