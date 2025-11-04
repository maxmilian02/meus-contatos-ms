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
    access_token = _get_access_token()
    if not access_token:
        return jsonify({"error": "not_authenticated"}), 401

    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get("https://graph.microsoft.com/v1.0/me/contacts?$top=200", headers=headers)
    
    # print(f"Status da Resposta da Graph API: {resp.status_code}")
    # print(f"Corpo da Resposta da Graph API: {resp.text}")

    if resp.status_code != 200:
        return jsonify({"error": "graph_error", "details": resp.text}), resp.status_code

    items = resp.json().get("value", [])
    grouped = defaultdict(list)

    # --- LÓGICA CORRIGIDA ---
    for contact in items:
        # Itera sobre cada endereço de e-mail de um único contato
        for email_entry in contact.get("emailAddresses", []):
            addr = email_entry.get("address")
            if addr and "@" in addr:
                domain = addr.split("@", 1)[1].lower()
                # Adiciona à lista, evitando duplicatas no mesmo domínio (opcional, mas bom)
                if addr not in grouped[domain]:
                    grouped[domain].append(addr)
    # -------------------------
            
    return jsonify(grouped)