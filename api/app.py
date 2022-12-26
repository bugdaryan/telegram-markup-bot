from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()


def create_app():
    app = Flask(__name__, template_folder='templates')
    login_manager = LoginManager(app)
    app.secret_key = Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    migrate.init_app(app, db)
    
    return app, login_manager

app, login_manager = create_app()