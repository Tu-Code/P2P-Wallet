from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jesus'
# OLD DB 
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
# NEW DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://pqnexjbnmaflvxct:pbow0ixqwgryzte7@kutnpvrhom7lki7u.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/sooev4l4e59owan5'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
migrate.init_app(app, db)


def create_database(app):
    if not path.exists('p2p/' + DB_NAME):
        print('Created Database!')

from .views import views
from .auth import auth

# from .controllers import controllers

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
# app.register_blueprint(controllers, url_prefix='/')

from .models import User

create_database(app)
db.create_all(app=app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    