#!env\Scripts\python.exe

import os
import flask
import functools

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

AUTHORIZATION_SCOPE = 'openid email profile'

AUTH_REDIRECT_URI = 'https://localhost:5000/genres'
BASE_URI = 'https://localhost:5000'
CLIENT_ID = ''
CLIENT_SECRET = ''


AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'

app = flask.Blueprint('google_auth', __name__)

def is_logged_in():
    return True if AUTH_TOKEN_KEY in flask.session else False

def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')
        
    oauth2_token = flask.session[AUTH_TOKEN_KEY]
    return google.oauth2.credentials.Credentials(
        oauth2_token['access_token'],
        refresh_token=oauth2_token['refresh_token'],
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri=ACCESS_TOKEN_URI
    )

def get_user_infor():
    credentials = build_credentials()
    oauth2_client = googleapiclient.discovery.build(
        'oauth2', 'v2',
        credentials=credentials
    )
    return oauth2_client.userinfo().get().execute()

# TODO: https://www.mattbutton.com/2019/01/05/google-authentication-with-python-and-flask/
# follow this link and the example on it.

