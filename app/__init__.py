from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# create database object globally but doesnot link yet
db = SQLAlchemy()


def create_app():
  app = Flask(__name__)
  print("app created")

  app.config['SECRET_KEY'] = 'yoursecretkey'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  # database object linked here
  # db.__init__(app)
  db.init_app(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  from .models import User

  @login_manager.user_loader
  def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

  from app.routes.auth import auth_bp
  from app.routes.tasks import task_bp
  app.register_blueprint(auth_bp)
  app.register_blueprint(task_bp)

  return app