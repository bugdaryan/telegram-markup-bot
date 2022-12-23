from flask import g
from models import User
from app import auth

@auth.verify_password
def verify_password(username_or_token, password):
    print('username_or_token: {}'.format(username_or_token))
    print('password: {}'.format(password))
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True