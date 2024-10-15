from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({'message': 'Welcome to FastShop!'})

@main.route('/products')
def products():
    # Example product list
    return jsonify([{'name': 'Product 1', 'price': 10.0}, {'name': 'Product 2', 'price': 15.0}])
