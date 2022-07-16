from flask import url_for, redirect, session
from flask_restx import reqparse
from services.oauth import get_google_oauth_client


def oauth_login():
    """Authenticate using google."""

    google = get_google_oauth_client()
    redirect_uri = url_for("v1.oauth_authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


def oauth_authorize():
    google = get_google_oauth_client()
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('welcome_page')


def welcome_page():
    name = dict(session)['profile']['name']
    return f'Hello, you are logged in as {name}!'