from flask import request, jsonify, abort, g
from models import User
from app import db, app, auth
from wonderwords import RandomWord
import string
import random
from config import Config
r = RandomWord() 

@app.route('/api/register', methods=['POST'])
def register():

    username, password = generate_random_username_password()
    
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    return (jsonify({'username': user.username, 'password': password}), 201)

@app.route('/api/login')
@auth.login_required
def get_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token, 'duration': 600})

def generate_random_username_password(existing_usernames=[]):

    username = generate_random_username()
    while username in existing_usernames:
        username = generate_random_username()
    
    letters = string.ascii_lowercase + string.digits
    password = ''.join(random.choice(letters) for i in range(Config.PASSWORD_LENGTH))

    return username, password

def generate_random_username():
    username = r.word(include_parts_of_speech=["adjectives"]) + '_' + r.word(include_parts_of_speech=["nouns"])
    return username