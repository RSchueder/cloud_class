import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from cloud_app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login' # function name of route that is login route
login_manager.login_message_category = 'info' 

mail = Mail()

def create_app(config_class = Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # name of the variable in the given route, instance of blueprint

    from cloud_app.users.routes import users 
    from cloud_app.posts.routes import posts 
    from cloud_app.classifications.routes import classifications 

    from cloud_app.main.routes import main 
    from cloud_app.info.routes import info

    from cloud_app.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(classifications)

    app.register_blueprint(main)
    app.register_blueprint(info)

    app.register_blueprint(errors)
    
    # create database by pushing context
    # add networks to the databased upon startup
    with app.app_context():
        if not os.path.exists('site.db'):
            db.create_all()


    return app