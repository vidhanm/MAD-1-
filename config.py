from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

# Create the extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['WTF_CSRF_ENABLED'] = False
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MAD1.sqlite3'
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Add a secret key for CSRF protection
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        from models import User,Influencer,Sponsor,Campaign, Request # Import the models
        db.create_all()
    
    return app

# Create the app
app = create_app()