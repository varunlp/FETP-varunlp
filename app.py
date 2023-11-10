from flask import Flask, redirect, url_for, session, render_template
from flask_oauthlib.client import OAuth
from datetime import datetime
import os
from collections.abc import MutableMapping

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['GOOGLE_ID'] = os.environ.get('GOOGLE_CLIENT_ID')  # Set your environment variable for Google Client ID
app.config['GOOGLE_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')  # Set your environment variable for Google Client Secret
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={'scope': 'email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
)

@app.route('/')
def home():
    if 'google_token' in session:
        user_info = google.get('userinfo')

        # Get user details
        user_name = user_info.data.get('name', 'User')
        user_email = user_info.data.get('email', 'user@example.com')

        # Get current time in India
        india_timezone = 'Asia/Kolkata'
        current_time = datetime.now().astimezone(timezone(india_timezone)).strftime('%Y-%m-%d %H:%M:%S')

        return render_template('home.html', user_name=user_name, user_email=user_email, current_time=current_time)
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('login'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    return redirect(url_for('home'))

@oauth.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)
