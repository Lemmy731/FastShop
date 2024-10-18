import os
import uuid
from flask import Flask, session,request, Response, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from database import create_app, db
from models import  User, Product
from datetime import datetime
from flask import jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

#database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fastshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
create_app(app)

#jwt
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)

jwt = JWTManager(app)



#signup 
@app.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
      
        # Get passwords from the request JSON body 
        data = request.get_json()
        password = data.get("password")
        confirmpassword = data.get("confirmpassword") # do i need confirm pass

        # Check if passwords match
        if password != confirmpassword:
            return jsonify({"error": "Passwords do not match!"}), 400

        # Hash the passw
        pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Get other signup data
        fullname = data.get("fullname")
        username = data.get("username")
        email = data.get("email")

        # Store new user in the database
        new_user = User(fullname=fullname, username = username, email=email, password=pw_hash)
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            return jsonify({"error": "User already exists!"}), 409

        # Return success message as JSON
        return jsonify({"message": "Account created!"}), 201


#login 
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        # Create a new token
        token = create_access_token(identity=user.username)
        return jsonify(access_token=token), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401


#logout
@app.route("/logout", methods=["POST"])
def logout():
    # Clear the session to log the user out
    session.clear()

    # Return a JSON response indicating the user is logged out
    return jsonify({"message": "Successfully logged out"}), 200


#get all products
@app.route("/products", methods=["GET"])
@jwt_required()
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

#update product by id
@app.route("/product/<int:id>", methods=["PUT"])
def update_product(id):
    # Get the updated product data from the request
    data = request.get_json()

    # Fetch the product by id from the database
    product = Product.query.get(id)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    # Extract updated values from the request 
    name = data.get("name")
    price = data.get("price")
    description = data.get("description")

    # Update product fields only if provided
    if name:
        product.name = name
    if price:
        product.price = price
    if description:
        product.description = description

    try:
        # Commit the changes to the database
        db.session.commit()
        return jsonify({
            "message": "Product updated successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description
            }
        }), 200  # 200 indicates a successful update
    except Exception as e:
        db.session.rollback()  # Rollback the transaction if something goes wrong
        return jsonify({"error": str(e)}), 500  # Internal server error
    

#delete product
@app.route("/product/<int:id>", methods=["DELETE"])
def delete_product(id):
    # Fetch the product by id from the database
    product = Product.query.get(id)

    # Check if product exists
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    try:
        # Delete the product from the database
        db.session.delete(product)
        db.session.commit()

        # Return success response
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback if something goes wrong
        return jsonify({"error": str(e)}), 500  # Return server error



