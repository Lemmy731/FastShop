from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from models import User, db
from flask import Blueprint

# Blueprint for your routes
auth_bp = Blueprint('auth', __name__)

# Signup Route
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    fullname = data.get("fullname")
    email = data.get("email")
    username = data.get("username")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists!"}), 409

    new_user = User(fullname=fullname, username=username, email=email, password=pw_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Account created successfully!"}), 201

# Login Route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create a JWT token
    token = create_access_token(identity=user.username)
    return jsonify(access_token=token), 200
