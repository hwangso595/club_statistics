import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import taipy.gui.builder as tgb
from db_util import get_database

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request
from taipy import Gui
from taipy.gui import navigate

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

usertype = "none"
@app.route("/login")
def login():
    usertype = request.args.get('user_type')
    return oauth.auth0.authorize_redirect(
        redirect_uri=f'{env.get("BASEURL")}/callback',
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    email = token['userinfo']['email']
    
    db = get_database()
    user_collection = db['users']
    user = json.dumps(user_collection.find_one({"email": email}), default=str)
    if not user:
        user_collection.insert_one({"email": email})
        user = json.dumps(user_collection.find_one({"email": email}), default=str)
    session['userinfo'] = user
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": env.get("BASEURL"),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

def get_user():
    return session['userinfo']['email'] if session and 'userinfo' in session else None, usertype

def get_app():
    return app