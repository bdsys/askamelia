import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

# Login for all HTTP methods besides POST
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    
    # Form input handling
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    # Query User table for first result of email matching email returned in form
    user = User.query.filter_by(email=email).first()

    # If the query doesn't return a user or the password is wrong
    # These are combined to prevent a brute force email signups check
    if not user or not check_password_hash(user.password, password):
        flash('Email or password is wrong, please check your credentials and try again.')
        return redirect(url_for('auth.login'))
    
    # If the query does return a user AND the password check passed from the above if,
    # Vend a session to the client via signed cookie
    ## and an additional signed cookie if the session is to be remembered via user input
    # redirect to protected view "main.profile"
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))
    
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


# All HTTP methods besides POST
@auth.route('/signup')
def signup():
    return render_template('signup.html')


# HTTP POST
@auth.route('/signup', methods=['POST'])
def signup_post():
    
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    # Query User table for the first matching email, if any, as a dupe checker.
    user = User.query.filter_by(email=email).first()
    
    if user: # if dupe checker is not None, redirect back to signup page for a retry
    
        # Pass a flash message to the next view, in this case the redirect to signup function
        flash('That email address already exists in this system!')
        
        return redirect(url_for('auth.signup'))
    
    else:
        
        # Create object for query to User table to create a new row
        new_user = User(
            email=email, 
            name=name, 
            password=generate_password_hash(
                password, 
                method='sha256'
            )
        )
        
        # Perform query and commit using the new_user object
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    

@auth.route('/logout')
@login_required # Can't logout a user that isn't logged in
def logout():
    logout_user() # Logs out user by invalidating their signed cookie on their client
    return redirect(url_for('main.index'))
