from flask import Blueprint, redirect, url_for, session, request, current_app, jsonify
import msal, os, time
from urllib.parse import urlencode

auth_bp = Blueprint("auth", __name__)

def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        current_app.config["MS_CLIENT_ID"],
        authority=current_app.config["MS_AUTHORITY"],
        client_credential=current_app.config["MS_CLIENT_SECRET"],
        token_cache=cache,
    )

@auth_bp.route("/auth/login")
def login():
    msal_app = _build_msal_app()
    scopes = ["User.Read", "Contacts.Read"]
    auth_url = msal_app.get_authorization_request_url(
        scopes,
        redirect_uri=current_app.config["MS_REDIRECT_URI"],
        response_type="code"
    )
    return redirect(auth_url)

@auth_bp.route("/auth/login/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "no_code"}), 400

    msal_app = _build_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=["User.Read", "Contacts.Read"],
        redirect_uri=current_app.config["MS_REDIRECT_URI"]
    )

    if "error" in result:
        return jsonify({"error": result}), 400

    # Save tokens minimally in session (for demo). In production use secure cookie or server-side store
    session["msal_token"] = {
        "access_token": result.get("access_token"),
        "refresh_token": result.get("refresh_token"),
        "expires_at": int(time.time()) + int(result.get("expires_in", 3600))
    }
    # redirect to frontend (UI route)
    return redirect(current_app.config["FRONTEND_URL"] + "/#/contatos")

@auth_bp.route("/auth/logout")
def logout():
    session.clear()
    # optionally redirect to MS logout
    logout_url = (
        "https://login.microsoftonline.com/common/oauth2/v2.0/logout?" +
        urlencode({"post_logout_redirect_uri": current_app.config["FRONTEND_URL"]})
    )
    return redirect(logout_url)
