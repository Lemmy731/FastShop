from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(app):
    
    # Initialize extensions
    db.init_app(app)

    # Creates the logs tables if the db doesnt already exist
    with app.app_context():
        db.create_all()
