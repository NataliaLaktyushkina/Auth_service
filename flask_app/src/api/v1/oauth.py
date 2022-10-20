from http import HTTPStatus

from flask import url_for, session, jsonify, request, make_response
from opentracing_decorator import Tracing

from database.db_service import create_user, create_social_account
from database.dm_models import User, SocialAccount
from services.oauth import get_oauth_client
from services.personal import auth
from utils.tracer import tracer, conditional_tracer

tracing = Tracing(tracer=tracer)


@conditional_tracer(tracer.start_as_current_span("oauth_login"))
def oauth_login():
    """Authenticate using social service."""
    social_service = request.values.get("social_service", None)
    oauth_client = get_oauth_client(social_service)
    if not oauth_client:
        return make_response('Could not find such a provider', HTTPStatus.NOT_FOUND)
    redirect_uri = url_for("v1.oauth_authorize",
                           social_service=social_service, _external=True)
    return oauth_client.authorize_redirect(redirect_uri)


@conditional_tracer(tracer.start_as_current_span("oauth_login"))
def oauth_authorize():
    social_service = request.values.get("social_service", None)
    oauth_client = get_oauth_client(social_service)
    if not oauth_client:
        return HTTPStatus.NOT_FOUND
    token = oauth_client.authorize_access_token()
    resp = oauth_client.get("userinfo", token=token)
    user_info = resp.json()

    session['profile'] = user_info
    session.permanent = True  # make the session permanent, so it keeps existing after browser gets closed
    social_acc_user = SocialAccount.get(social_id=user_info['id'],
                                        social_name=social_service,
                                        email=user_info['email'])
    if social_acc_user is None:
        user = create_user(username=user_info['name'],
                           email=user_info['email'])
        social_acc_user = create_social_account(
            social_id=user_info['id'],
            social_name=social_service,
            user_id=user.id)

    user = User.query.filter_by(id=social_acc_user.user_id).first()
    jwt_tokens = auth.get_jwt_tokens(user)
    return jsonify(access_token=jwt_tokens['access_token'],
                   refresh_token=jwt_tokens['refresh_token'])
