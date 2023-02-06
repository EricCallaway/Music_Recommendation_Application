from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "music_app"

"""
Creating Flask Application, initializing the secret key, and returning the app
"""


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5uP3rSec#tK3%'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:Eric19$$@localhost/{DB_NAME}'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
 

    #Importing and registering views for application
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    

    from .models import User, Note

    create_database(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
