"""
get_connection.py
A module that creates a connection to the PowerSchool API.
"""

import base64
import requests
import keyring
from constants import AUTH_URL

# Various other variables.
API_CLIENT_ID = keyring.get_password("PS-API-ID", "PS-API")
API_CLIENT_SECRET = keyring.get_password("PS-API-SECRET", "PS-API")


def get_connection():
    """
    Retrieves a connection to the API by sending a POST request to the AUTH_URL with the provided
    API_CLIENT_ID and API_CLIENT_SECRET.

    Returns:
        list: A list containing the access token and token type retrieved from the API response.
    """
    headers = {
        "Authorization": "Basic "
        + base64.b64encode(
            bytes(API_CLIENT_ID + ":" + API_CLIENT_SECRET, "utf-8")
        ).decode("utf-8")
    }
    payload = {"grant_type": "client_credentials"}

    response = requests.post(AUTH_URL, headers=headers, data=payload, timeout=10)
    data = response.json()
    str_access_token = data["access_token"]
    local_token_type = data["token_type"]
    return [str_access_token, local_token_type]
