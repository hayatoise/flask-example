from typing import Text

from flask import render_template, redirect, url_for, Blueprint, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from application.models import User
from application.database import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login() -> Text:
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['GET'])
def signup() -> Text:
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    display_name = request.form.get('display_name')
    email = request.form.get('email')
    password = request.form.get('password')

    user_by_name = User.query.filter_by(name=name).first()

    if user_by_name:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    user_by_email = User.query.filter_by(email=email).first()

    if user_by_email:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(name=name, display_name=display_name, email=email,
                    password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
