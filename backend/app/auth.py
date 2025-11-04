import uuid
from flask import Blueprint, redirect, url_for, session, request, current_app, jsonify
import msal
import time
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
    state = str(uuid.uuid4())
    session["oauth_state"] = state
    session.modified = True
    
    msal_app = _build_msal_app()
    scopes = ["User.Read", "Contacts.Read"]
    
    auth_url = msal_app.get_authorization_request_url(
        scopes,
        state=state,
        redirect_uri=current_app.config["MS_REDIRECT_URI"],
        prompt='select_account'
    )
    
    return redirect(auth_url)


@auth_bp.route("/auth/login/callback")
def callback():
    received_state = request.args.get('state')
    session_state = session.get("oauth_state")
    
    if not received_state or received_state != session_state:
        return jsonify({"error": "state_mismatch", "details": "Invalid state parameter"}), 400

    code = request.args.get("code")
    if not code:
        error = request.args.get("error", "unknown_error")
        error_description = request.args.get("error_description", "No code returned")
        return jsonify({
            "error": error, 
            "details": error_description
        }), 400

    msal_app = _build_msal_app()
    
    try:
        result = msal_app.acquire_token_by_authorization_code(
            code,
            scopes=["User.Read", "Contacts.Read"],
            redirect_uri=current_app.config["MS_REDIRECT_URI"]
        )
    except Exception as e:
        return jsonify({"error": "token_acquisition_failed", "details": str(e)}), 500

    if "error" in result:
        return jsonify({"error": "msal_error", "details": result}), 400
    
    session.pop("oauth_state", None)
    
    session["msal_token"] = {
        "access_token": result.get("access_token"),
        "refresh_token": result.get("refresh_token"),
        "expires_at": int(time.time()) + int(result.get("expires_in", 3600))
    }
    session["is_authenticated"] = True
    session.modified = True

    return redirect(current_app.config["FRONTEND_URL"] + "/contatos")


@auth_bp.route("/auth/status")
def status():
    is_authenticated = session.get("is_authenticated", False)
    return jsonify({"is_authenticated": is_authenticated})


@auth_bp.route("/auth/logout")
def logout():
    # Limpa a sessão local da aplicação
    session.clear()
    
    # Redireciona de volta para a tela de login no frontend
    # sem deslogar da conta da Microsoft
    return redirect(current_app.config["FRONTEND_URL"])