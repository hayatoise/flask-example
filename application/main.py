from typing import Text

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from application.models import User

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index() -> Text:
    users = User.query.all()
    return render_template('index.html', users=users)


@main.route('/@<name>', methods=['GET'])
def profile(name) -> Text:
    user = User.query.filter_by(name=name).first()
    if not user:
        return redirect(url_for('main.index'))
    return render_template('profile.html', name=user.name, display_name=user.display_name)


@main.route('/settings/account', methods=['GET'])
@login_required
def settings() -> Text:
    return render_template('settings.html', email=current_user.email)
