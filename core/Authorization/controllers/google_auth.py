
from flask import redirect, url_for, session, request, Blueprint
from flask_oauthlib.client import OAuth


google_login_bp = Blueprint('google_login', __name__)

oauth = OAuth()
google = oauth.remote_app(
    'google',
    consumer_key='868117847269-k8p59v6qtruipkm3jdb7ma1el4c64n2h.apps.googleusercontent.com',
    consumer_secret='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',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@google_login_bp.route('/login')
def login():
    return google.authorize(callback=url_for('google_login.authorized', _external=True))

@google_login_bp.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('test.testing'))

@google_login_bp.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={}, error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


