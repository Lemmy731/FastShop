from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from config import DevelopmentConfig
from auth import auth_bp  #auth routes
from product import product_blueprint  # Product CRUD routes

app = Flask(__name__)

# configuration
app.config.from_object(DevelopmentConfig)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(product_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
