import os
from . import db, create_app, models
from .models import User
from werkzeug.security import generate_password_hash

print("Creating SQLite database...")
db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.
print("Created!")

print("Seeding initial application dependencies...")
print("Creating single user...")

# If single user doesn't exist, create with env var password

single_user_email = os.getenv('FLASK_AAW_USER_EMAIL')

# Query User table for the first matching email, if any, as a dupe checker.
user = User.query.filter_by(email=single_user_email).first()

if user: # if dupe checker is not None, redirect back to signup page for a retry

    print(f"Single user exists -- {os.getenv('FLASK_AAW_USER_EMAIL')}")

else:

    print("Single user for the app doesn't exist, creating...")
    print(f"Email: {os.getenv('FLASK_AAW_USER_EMAIL')}")
    
    single_user_password = os.getenv('FLASK_AAW_USER_PASSWORD')

    # Create object for query to User table to create a new row
    new_user = User(
        email=single_user_email, 
        name="single-user",
        password=generate_password_hash(
            single_user_password,
            method='sha256'
        )
    )
    
    # Perform query and commit using the new_user object
    db.session.add(new_user)
    db.session.commit()