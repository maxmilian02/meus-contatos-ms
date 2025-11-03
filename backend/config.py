import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "devkey")
    CLIENT_ID = os.getenv("MS_CLIENT_ID")
    CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("MS_REDIRECT_URI")
    AUTHORITY = os.getenv("MS_AUTHORITY", "https://login.microsoftonline.com/common")
