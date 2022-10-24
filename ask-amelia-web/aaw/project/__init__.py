import os
from flask import Flask # framework
from flask_sqlalchemy import SQLAlchemy # ORM
from flask_login import LoginManager # framework's session tracker
from werkzeug.security import generate_password_hash

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    # Define login manager
    login_manager = LoginManager() # Create object
    login_manager.login_view = 'auth.login' # Tell login manager where sessions are vendored
    login_manager.init_app(app)
    
    # Allows references to the User table
    from .models import User

    # User loader Decoractor telling the login manager what property, in this case the pk since it's always unique, 
    # of User table to use for handing out unique sessions per authenticated user.
    @login_manager.user_loader
    def load_user(user_id):
        # This user loader function is used by the login manager to identify users in the User table by the table's PK
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # # If single user doesn't exist, create with env var password
    
    # single_user_email = os.getenv('FLASK_AAW_USER_EMAIL')
    
    # # Query User table for the first matching email, if any, as a dupe checker.
    # user = User.query.filter_by(email=single_user_email).first()
    
    # if user: # if dupe checker is not None, redirect back to signup page for a retry
    
    #     print("Single user for the app doesn't exist, creating...")
    #     print(f"Email: {os.getenv('FLASK_AAW_USER_EMAIL')}")
        
    #     single_user_password = os.getenv('FLASK_AAW_USER_PASSWORD')
    
    #     # Create object for query to User table to create a new row
    #     new_user = User(
    #         email=single_user_email, 
    #         name="single-user",
    #         password=generate_password_hash(
    #             single_user_password,
    #             method='sha256'
    #         )
    #     )
        
    #     # Perform query and commit using the new_user object
    #     db.session.add(new_user)
    #     db.session.commit()
    
    # else:
        
    #     print(f"Single user exists -- {os.getenv('FLASK_AAW_USER_EMAIL')}")

    return app
