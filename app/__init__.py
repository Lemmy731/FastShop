from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_pyfile('config.py')

    # Initialize extensions
    db.init_app(app)

    # Register routes (Import from routes.py)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
