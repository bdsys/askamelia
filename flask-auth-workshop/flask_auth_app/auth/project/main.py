from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required # Decorator to protect route from unauthenticated users
def profile():
    # curent_user represents the ORM object, User in this case, that login_manager
    # used to authenticate the user via signed cookie on the client side
    return render_template('profile.html', name=current_user.name)
