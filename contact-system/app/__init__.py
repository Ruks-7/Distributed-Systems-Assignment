from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail
from config import Config

mongo = PyMongo()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    mongo.init_app(app)
    mail.init_app(app)
    
    from .routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    return app