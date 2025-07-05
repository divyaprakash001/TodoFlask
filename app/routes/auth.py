# routes for login and logout

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

auth_bp = Blueprint('auth',__name__)


USER_CREDENTIALS  = {
  'username':'admin',
  'password':'1234'
}


@auth_bp.route('/login')
def login():
    return render_template('login.html')


@auth_bp.route('/login',methods=['POST'])
def login_post():
  if request.method == 'POST':
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password,password):
      flash('Please check your login details and try again.')
      return redirect(url_for('auth.login'))
    
    flash('Login Successful')
    login_user(user,remember=False)
    return redirect(url_for('tasks.view_tasks'))


@auth_bp.route("/signup")
def signup():
  return render_template('register.html')

@auth_bp.route("/signup",methods=['POST'])
def signup_post():
  if request.method == 'POST':
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
      flash("User with email already exists!")
      return redirect(url_for('auth.signup'))
    
    new_user = User(email=email,name=name,password=generate_password_hash(password,method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))



@auth_bp.route('/logout')
def logout():
  logout_user()
  flash("Logged out","info")
  return redirect(url_for('auth.login'))
