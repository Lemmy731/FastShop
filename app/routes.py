from flask import Blueprint, jsonify
from flask import session,render_template,request, Response, redirect, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from db import db_init, db
from models import  User, Product
from datetime import datetime
from flask_session import Session
from helpers import login_required

main = Blueprint('main', __name__)


#sign up
@main.route("/signup", methods=["Get", "Post"])
def signup():

    return jsonify({'message': 'Welcome to FastShop!'})


@main.route("/products")
def products():
    # Example product list
    return jsonify([{'name': 'Product 1', 'price': 10.0}, {'name': 'Product 2', 'price': 15.0}])
