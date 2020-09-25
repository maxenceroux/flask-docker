import datetime, time
import os
import requests
from flask import Flask, render_template, redirect, url_for, request, flash, make_response, session
from forms import SignupForm
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.parse
import random, string
import json, base64
import rand
from models import Flowers, Users
from database import db_session
import logging
from functions import get_logins_spotify, createStateKey, getToken, makeGetRequest, getUserInformation, getUserSavedAlbums, getBackGroundColors
from app import app

@app.route("/success")
def success():
    return "Thank you de t'être enregistré.e"

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method=="GET":
        return render_template('login.html')
    if request.method=="POST":
        email=request.form.get('email')
        password = request.form.get('password')
        remember=True if request.form.get('remember') else False

        user = Users.query.filter_by(email=email).first()
        session['email'] =email
        if not user or not check_password_hash(user.mdp, password):
            flash('Please check your login details and try again.')
            return redirect(f"http://localhost:8080/{url_for('login')}")
        login_user(user, remember=remember)
        return redirect(f"http://localhost:8080/{url_for('profile')}")



@app.route('/authorize')
def authorize():
	client_id = 'b45b68c4c7a0421589605adf1e1a7626'
	# client_secret = app.config['CLIENT_SECRET']
	redirect_uri = "http://localhost:8080/callback"
	scope = "user-library-read"

	# state key used to protect against cross-site forgery attacks
	state_key = createStateKey(15)
	session['state_key'] = state_key

	# redirect user to Spotify authorization page
	authorize_url = 'https://accounts.spotify.com/en/authorize?'
	parameters = 'response_type=code&client_id=' + client_id + '&redirect_uri=' + redirect_uri + '&scope=' + scope + '&state=' + state_key
	response = make_response(redirect(authorize_url + parameters))
	return response

@app.route('/callback')
def callback():
    # make sure the response came from Spotify
    if request.args.get('state') != session['state_key']:
        return render_template('index.html', error='State failed.')
    if request.args.get('error'):
        return render_template('index.html', error='Spotify error.')
    else:
        code = request.args.get('code')
        logging.warning(code)
        session.pop('state_key', None)

        # get access token to make requests on behalf of the user
        payload = getToken(code)
        logging.warning(payload)
        if payload != None:
            session['token'] = payload[0]
            session['refresh_token'] = payload[1]
            session['token_expiration'] = time.time() + payload[2]
        else:
            return redirect('http://localhost:8080/error')

    current_user = getUserInformation(session)
    logging.warning(current_user)
    session['display_name'] = current_user['display_name']

    return redirect(session['previous_url'])


@app.route('/login_spotify', methods=('GET', 'POST'))
def login_spotify():
    if session.get('token') == None or session.get('token_expiration') == None:
        session['previous_url'] = 'http://localhost:8080/profile'
        logging.warning('inlogin')
        return redirect("http://localhost:8080/authorize")
    return render_template('profile.html', display_name=session['display_name'])

@app.route('/error')
def error():
    return("no")

@app.route('/signups', methods=('GET', 'POST'))
def signups():
    if request.method=="GET":
        return render_template('signups.html')
    if request.method=="POST":            
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            return redirect(f"http://localhost:8080/{url_for('login')}")
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = Users(email=email, utilisateur=name, mdp=generate_password_hash(password, method='sha256'),date_creation=datetime.datetime.now(),date_modification=datetime.datetime.now())
        # add the new user to the database
        db_session.add(new_user)
        db_session.commit()
        return redirect(f"http://localhost:8080/{url_for('login')}")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(f"http://localhost:8080/{url_for('index')}")

@app.route('/s')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.utilisateur)

@app.route('/albums')
@login_required
def albums():
    saved_albums=getUserSavedAlbums(session)
    colors = getBackGroundColors()
    # saved_albums=saved_albums['items'][2]['album']['images'][0]['url']
    images = []
    artists=[]
    album_names=[]
    for i in range(20):
        images.append(saved_albums['items'][i]['album']['images'][0]['url'])
        artists.append(saved_albums['items'][i]['album']['artists'][0]['name'])
        album_names.append(saved_albums['items'][i]['album']['name'])

    return render_template('albums.html', images = images, artists= artists, album_names=album_names, colors=colors[0])

@app.route("/", methods=('GET', 'POST'))
def signup():
    if request.method=="POST":
    # form = SignupForm()
    # if form.validate_on_submit():
        user = Users(utilisateur=request.form["username"], email=request.form["email"], mdp=request.form["password"], date_creation=datetime.datetime.now(),date_modification=datetime.datetime.now())
        db_session.add(user)
        db_session.commit()
        return redirect(f"http://localhost:8080/{url_for('success')}")
    session.clear()
    return render_template('base.html')
