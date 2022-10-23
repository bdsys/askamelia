from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

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
        
        return redirect(url_for('auth.login'))
    
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
def logout():
    return 'Logout'
