from flask import Flask, request, redirect, render_template, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time

import musictaste
import os
import spotipy
from helpers import apology
import base64
from werkzeug.exceptions import HTTPException

from flask_session import Session


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = os.urandom(24)

os.environ['CLIENT_ID'] = "ea31cee76f264dc996539e24958738f1"
os.environ['SECRET_KEY'] = "f5569d0187ed4350b51850169f48fe7d"
os.environ['SECRET_KEY'] = 'http://127.0.0.1:5000/callback/'

client_id = os.environ.get("CLIENT_ID") 
secret_key = os.environ.get("SECRET_KEY") 
redirect_uri = os.environ.get("REDIRECT_URI")

scope = "user-read-recently-played user-top-read"

os.environ.get("client_id") 

# ----------------------- AUTH API PROCEDURE -------------------------

def valid_token(resp):
    return resp is not None and not 'error' in resp

# prevent cached responses
@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response

@app.errorhandler(HTTPException)
def handle_exception(e):
    return apology("error", 404)

# -------------------------- API REQUESTS ----------------------------
@app.route("/")
def home():
    session.clear()
    return render_template('home.html')

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/visualize")


@app.route('/visualize')
def visualize():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        sp_oath = create_spotify_oauth()
        auth_url = sp_oath.get_authorize_url()
        return redirect(auth_url)

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    # get user's recently played tracks and collect the artist(s)'s data
    results = sp.current_user_recently_played(limit=50, after=None, before=None)
    list = []
    list.append(results)
    session['recently_played_json'] = list

    # get user's top short-term artists
    results = sp.current_user_top_artists(limit=50,offset=0,time_range='short_term')
    list = []
    list.append(results)
    session['short_artists_json'] = list

    # get user's top medium-term artists
    results = sp.current_user_top_artists(limit=50,offset=0,time_range='medium_term')
    list = []
    list.append(results)
    session['med_artists_json'] = list

    # get user's top long-term artists
    results = sp.current_user_top_artists(limit=50,offset=0,time_range='long_term')
    list = []
    list.append(results)
    session['long_artists_json'] = list

    # test token
    recently_played = sp.current_user_recently_played()
    
    # if the token is valid, continue to next step: plotting data
    if valid_token(recently_played):
        try:
            # create buffer with image of music map
            buffer = musictaste.main(sp, session['recently_played_json'], session['short_artists_json'], session['med_artists_json'], session['long_artists_json'])
            buffer.seek(0)
            # encode buffer
            image_memory = base64.b64encode(buffer.getvalue())
            # render index.html and pass decoded buffer
            return render_template("index.html", img_data=image_memory.decode('utf-8'))
        except BaseException:
            return apology("error", 403)


# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=client_id,
            client_secret=secret_key,
            redirect_uri=url_for('callback', _external=True),
            scope=scope)

if __name__ == "__main__":
    app.run()
