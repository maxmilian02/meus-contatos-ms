from flask import Blueprint, jsonify, session
import requests
from collections import defaultdict
import time

contacts_bp = Blueprint("contacts", __name__)

@contacts_bp.route("/", methods=["GET"])
def list_contacts():
    token = session.get("token")
    if not token:
        return jsonify({"error": "not_authenticated"}), 401

    headers = {"Authorization": f"Bearer {token['access_token']}"}
    resp = requests.get("https://graph.microsoft.com/v1.0/me/contacts", headers=headers)

    if resp.status_code != 200:
        return jsonify({"error": "graph_api_error", "details": resp.text}), 500

    contacts = resp.json().get("value", [])
    grouped = defaultdict(list)
    for contact in contacts:
        email = contact.get("emailAddresses", [{}])[0].get("address")
        if email:
            domain = email.split("@")[-1]
            grouped[domain].append(email)

    return jsonify(grouped)
