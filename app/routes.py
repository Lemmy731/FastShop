import os
import uuid
from flask import Flask, session,render_template,request, Response, redirect, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from database import create_app, db
from models import  User, Product
from datetime import datetime
from flask_session import Session
from help import login_required
from flask import jsonify, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fastshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
create_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#signup 
@app.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        # Clear any existing session
        session.clear()

        # Get passwords from the request JSON body (instead of form data)
        data = request.get_json()
        password = data.get("password")
        confirmpassword = data.get("confirmpassword")

        # Check if passwords match
        if password != confirmpassword:
            return jsonify({"error": "Passwords do not match!"}), 400

        # Hash the passw
        pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Get other signup data
        fullname = data.get("fullname")
        email = data.get("email")

        # Store new user in the database
        new_user = User(fullname=fullname, email=email, password=pw_hash)
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            return jsonify({"error": "User already exists!"}), 409

        # Return success message as JSON
        return jsonify({"message": "Account created!"}), 201


#login as merchant
@app.route("/login", methods=["POST"])
def login():
    # Clear any existing session
    session.clear()

    # Get the username and password from the request body (JSON)
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Query the database to find the user by username
    result = User.query.filter_by(email=email).first()

    # Ensure the user exists and the password is correct
    if result is None or not check_password_hash(result.password, password):
        return jsonify({"error": "Invalid email and/or password"}), 401

    # Store the username in the session (user is logged in)
    session["email"] = result.email

    # Respond with a success message
    return jsonify({"message": "Login successful", "email": result.email}), 200


#logout
@app.route("/logout", methods=["POST"])
def logout():
    # Clear the session to log the user out
    session.clear()

    # Return a JSON response indicating the user is logged out
    return jsonify({"message": "Successfully logged out"}), 200


#get all products
@app.route("/products", methods=["GET"])
def get_all_products():
    # Query all products from the database
    products = Product.query.all()

    # Convert products into a list of dictionaries
    products_list = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        } for product in products
    ]

    # Return the products as JSON
    return jsonify(products_list), 200



#add product
@app.route("/products", methods=["POST"])
def add_product():
    # Get the data from the request body (assumes JSON is sent)
    data = request.get_json()

    # Extract product details from the JSON data
    name = data.get("name")
    price = data.get("price")
    description = data.get("description")

    # Validate the required fields
    if not name or not price:
        return jsonify({"error": "Name and price are required fields"}), 400

    # Create a new product object
    new_product = Product(
        name=name,
        price=price,
        description=description
    )

    # Add the new product to the database
    try:
        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Roll back the transaction in case of an error
        return jsonify({"error": "Could not add product", "details": str(e)}), 500

    # Return a success response with the product details
    return jsonify({
        "message": "Product added successfully",
        "product": {
            "id": new_product.id,
            "name": new_product.name,
            "price": new_product.price,
            "description": new_product.description
        }
    }), 201  # 201 status code for resource creation


