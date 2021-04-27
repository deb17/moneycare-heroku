from flask import Flask, redirect, request, abort, url_for
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)


app.config['SECRET_KEY'] = '5ad1b20f9e1a66492a68e490e5abfb7d'
app.config['GOOGLE_OAUTH_CLIENT_ID'] = '737155067926-jpco79782ombb1c068ifj9gln8ea7has.apps.googleusercontent.com'
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = 'YJv1OLtf9sSkHntlHiHBcwCZ'
app.config['OAUTHLIB_RELAX_TOKEN_SCOPE'] = True

google_blueprint = make_google_blueprint(
    scope=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'],
    redirect_to='google_login'
)


@app.route('/')
def index():

    url = request.url.replace(
        'https://debs-moneycare.herokuapp.com/',
        'https://moneycare.pythonanywhere.com/google/authorized'
    )

    if url == request.url:
        abort(400)

    return redirect(url)


@app.route('/google-login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))

    resp = google.get('/oauth2/v1/userinfo')
    retval = resp.json()
    print('RETVAL', retval)
    gname = retval['name']
    gmail = retval['email']

    url = f'https://moneycare.pythonanywhere.com/google-login?name={gname}&email={gmail}'

    return redirect(url)
