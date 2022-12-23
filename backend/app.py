from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restx import Api
from config import Config


from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='Markup bot', description='Markup bot API documentation', doc='/docs')


    app.secret_key = Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # login_manager = LoginManager()
    # login_manager.session_protection = "strong"
    # login_manager.login_view = "login"
    # login_manager.login_message_category = "info"


    # login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    return app, api

app, api = create_app()