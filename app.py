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
from functions import get_logins_spotify, createStateKey, getToken, makeGetRequest, getUserInformation
import routes

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Users.query.get(int(user_id))


if __name__ == '__main__':
    from api import *
    
    app.run(host='0.0.0.0', port=5090, debug=True)
