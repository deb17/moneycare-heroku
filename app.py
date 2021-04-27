import os

from flask import Flask, redirect, url_for
from werkzeug.urls import url_encode
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = (
    os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
)
app.config['OAUTHLIB_RELAX_TOKEN_SCOPE'] = True

google_blueprint = make_google_blueprint(
    scope=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'],
    redirect_to='google_login'
)
app.register_blueprint(google_blueprint)


@app.route('/google-login')
def google_login():

    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v1/userinfo')
    data = resp.json()
    retval = {}
    retval['name'] = data['name']
    retval['email'] = data['email']

    url = (
        'https://moneycare.pythonanywhere.com/google-login?' +
        url_encode(retval)
    )

    return redirect(url)
