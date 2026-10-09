import base64
import hashlib
import json
import os
import secrets

import requests

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

API_PATH = os.path.join(CURRENT_FILE_DIR, "api.json")

with open(API_PATH, "r") as f:
    API = json.load(f)


def refresh_token(client_id, client_secret, refresh_token):
    request_body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    response = requests.post(
        "https://auth.atlassian.com/oauth/token",
        json=request_body,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )

    response.raise_for_status()
    return response.json()


def get_access_token():

    response = refresh_token(
        API["client_id"], API["client_secret"], API["refresh_token"]
    )
    print(response)

    API["access_token"] = response["access_token"]
    API["refresh_token"] = response["refresh_token"]

    with open(API_PATH, "w") as f:
        json.dump(API, f)

    print("New auth json created.")
    return response["access_token"]
