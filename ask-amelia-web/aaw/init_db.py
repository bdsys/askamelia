import os
from project import db, create_app, models
from project.models import User, AccessCodes
from werkzeug.security import generate_password_hash

print("Starting DB maintenance...")

print("Creating SQLite database...")

db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.

print("Created!")

print("Seeding initial application dependencies...")

app = create_app()

print("Creating single user...")

# If single user doesn't exist, create with env var password

single_user_email = os.getenv('FLASK_AAW_USER_EMAIL')

with app.app_context():
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
        
        print("Single user created!")
        
print("Finished with single user seed.")
        
print("Seeding access codes...")

# Use SSM PS string list in the future...for now os.getenv

# If access code doesn't exist, create

access_code_envvar_1 = os.getenv('FLASK_AAW_ACESS_CODE_1')

with app.app_context():
    # Query User table for the first matching email, if any, as a dupe checker.
    access_code_query = AccessCodes.query.filter_by(access_code=access_code_envvar_1).first()
    
    if access_code_query: # if dupe checker is not None, redirect back to signup page for a retry
    
        print(f"Access code exists -- {os.getenv('access_code_envvar_1')}")

    else:

        print("Access code for the app doesn't exist, creating...")
        print(f"Access code: {os.getenv('access_code_envvar_1')}")
        
        # Create object for query to User table to create a new row
        new_access_code = AccessCodes(
            access_code=access_code_envvar_1,
        )
        
        # Perform query and commit using the new_user object
        db.session.add(new_access_code)
        db.session.commit()
        
        print("New access code created!")
print("Finished with access codes.")

print("DB seeding is finished!")

print("DB maintenance is finished!")
