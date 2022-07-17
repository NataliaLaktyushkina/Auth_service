from flask import url_for, redirect, session, jsonify
from flask_restx import reqparse
from services.oauth import get_google_oauth_client
from services.personal import auth
from database.dm_models import User, SocialAccount
from database.db_service import create_user, create_social_account


def oauth_login():
    """Authenticate using google."""

    google = get_google_oauth_client()
    redirect_uri = url_for("v1.oauth_authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


def oauth_authorize():
    google = get_google_oauth_client()
    token = google.authorize_access_token()
    resp = google.get("userinfo", token=token)
    user_info = resp.json()

    session['profile'] = user_info
    session.permanent = True  # make the session permanent, so it keeps existing after browser gets closed

    social_acc_user = SocialAccount.get(social_id=user_info['id'],
                                       social_name=user_info['name'],
                                       email=user_info['email'])
    if social_acc_user is None:
        user = create_user(username=user_info['name'],
                           email=user_info['email'])
        social_acc_user = create_social_account(
            social_id=user_info['id'],
            social_name=user_info['name'],
            user_id=user.id)

    user = User.query.filter_by(id=social_acc_user.user_id).first()
    jwt_tokens = auth.get_jwt_tokens(user)
    return jsonify(access_token=jwt_tokens['access_token'],
                   refresh_token=jwt_tokens['refresh_token'])


