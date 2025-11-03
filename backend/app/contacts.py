from flask import Blueprint, session, jsonify, current_app
import requests
from collections import defaultdict
import time

contacts_bp = Blueprint("contacts", __name__)

def _get_access_token():
    token = session.get("msal_token")
    if not token:
        return None
    if token.get("expires_at", 0) <= int(time.time()):
        return None
    return token.get("access_token")

@contacts_bp.route("/contacts", methods=["GET"])
def list_contacts():
    """
    Returns grouped contacts by domain:
    { "gmail.com": ["a@gmail.com", ...], "contoso.com": [...] }
    """
    access_token = _get_access_token()
    if not access_token:
        return jsonify({"error": "not_authenticated"}), 401

    headers = {"Authorization": f"Bearer {access_token}"}
    # get contacts from Graph (pagination simplified - get first page)
    resp = requests.get("https://graph.microsoft.com/v1.0/me/contacts?$top=200", headers=headers)
    if resp.status_code != 200:
        return jsonify({"error": "graph_error", "details": resp.text}), resp.status_code

    items = resp.json().get("value", [])
    grouped = defaultdict(list)
    for c in items:
        emails = c.get("emailAddresses", [])
        if emails:
            addr = emails[0].get("address")
            if addr and "@" in addr:
                domain = addr.split("@", 1)[1].lower()
                grouped[domain].append(addr)
    return jsonify(grouped)
