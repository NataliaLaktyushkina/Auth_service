from flask import url_for, redirect
from flask_restx import reqparse
from services.oauth import get_google_oauth_client


def oauth_login():
    """Authenticate using google."""

    google = get_google_oauth_client()
    redirect_uri = url_for("v1.oauth_authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


# google_authorize_parser = reqparse.RequestParser()
# location argument - specify alternate locations to pull the values from
# google_authorize_parser.add_argument("User-Agent", location="headers")

def oauth_authorize():
    google = get_google_oauth_client()
    token = google.authorize_access_token()
    resp = google.get('account/verify_credentials.json')
    resp.raise_for_status()
    profile = resp.json()
    # do something with the token and profile
    return redirect('/')