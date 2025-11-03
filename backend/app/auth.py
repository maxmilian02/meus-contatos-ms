# app/auth.py
from flask import Blueprint, redirect, request, session
import msal, os

auth_bp = Blueprint("auth", __name__)

CLIENT_ID = os.environ.get("MS_CLIENT_ID")
CLIENT_SECRET = os.environ.get("MS_CLIENT_SECRET")
AUTHORITY = os.environ.get("MS_AUTHORITY", "https://login.microsoftonline.com/common")
REDIRECT_URI = os.environ.get("MS_REDIRECT_URI")
SCOPES = ["User.Read", "Contacts.Read"]

@auth_bp.route("/auth/login")
def login():
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    auth_url = msal_app.get_authorization_request_url(
        SCOPES, redirect_uri=REDIRECT_URI
    )
    return redirect(auth_url)

@auth_bp.route("/auth/login/callback")
def authorized():
    code = request.args.get("code")
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    result = msal_app.acquire_token_by_authorization_code(
        code, SCOPES, redirect_uri=REDIRECT_URI
    )
    session["user"] = result.get("id_token_claims")
    return "Login OK, token recebido."
