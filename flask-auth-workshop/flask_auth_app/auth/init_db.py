from project import db, create_app, models

print("Creating SQLite database...")

db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.

print("Created!")
