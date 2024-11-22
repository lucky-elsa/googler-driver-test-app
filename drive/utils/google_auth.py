import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

SCOPES = ['https://www.googleapis.com/auth/drive']

CREDENTIALS_FILE = os.path.join(os.getcwd(), 'credentials.json')
TOKEN_FILE = os.path.join(os.getcwd(), 'token.json')

def get_flow():
    return Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/drive/callback'
    )

def save_credentials(credentials):
    with open(TOKEN_FILE, 'w') as token_file:
        token_file.write(credentials.to_json())

def load_credentials():
    if os.path.exists(TOKEN_FILE):
        return Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    return None
