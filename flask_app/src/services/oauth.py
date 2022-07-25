import os
import sys

sys.path.append(os.path.dirname(__file__) + '/..')
from utils.settings import get_oauth_settings

google = None
oauth_settings = get_oauth_settings()


def register_google(oauth_client):
    return oauth_client.register(
        name="google",
        client_id=oauth_settings.GOOGLE_CLIENT_ID,
        client_secret=oauth_settings.GOOGLE_CLIENT_SECRET,
        access_token_url=oauth_settings.GOOGLE_ACCESS_TOKEN_URL,
        authorize_url=oauth_settings.GOOGLE_AUTHORIZE_URL,
        api_base_url=oauth_settings.GOOGLE_API_BASE_URL,
        client_kwargs={"scope": "profile email"},
    )


def get_oauth_client(client_name):
    if client_name =='google':
        return google
    return None
