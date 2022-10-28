import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

# Login for all HTTP methods besides POST
@auth.route('/invitation')
def invitation():
    return render_template('invitation.html')

@auth.route('/invitation', methods=['POST'])
def invitation_post():
    
    # Form input handling
    email = os.getenv('FLASK_AAW_USER_EMAIL')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    # Query User table for first result of email matching email returned in form
    user = User.query.filter_by(email=email).first()

    # If the query doesn't return a user or the password is wrong
    # These are combined to prevent a brute force email signups check
    if not user or not check_password_hash(user.password, password):
        flash('The invitation code you entered doesn''t seem right. Try again?')
        return redirect(url_for('auth.invitation'))
    
    # If the query does return a user AND the password check passed from the above if,
    # Vend a session to the client via signed cookie
    ## and an additional signed cookie if the session is to be remembered via user input
    # redirect to protected view "main.profile"
    login_user(user, remember=remember)
    return redirect(url_for('main.subject'))    


@auth.route('/logout')
@login_required # Can't logout a user that isn't logged in
def logout():
    logout_user() # Logs out user by invalidating their signed cookie on their client
    return redirect(url_for('auth.invitation'))
