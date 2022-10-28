import os
from flask import Flask # framework
from flask_sqlalchemy import SQLAlchemy # ORM
from flask_login import LoginManager # framework's session tracker

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(
        __name__,
        static_url_path='',
        static_folder='templates',
        template_folder='static',
    )

    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    # Define login manager
    login_manager = LoginManager() # Create object
    login_manager.login_view = 'auth.invitation' # Tell login manager where sessions are vendored
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

    return app
