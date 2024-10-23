from flask import Blueprint, jsonify, request
from models import db, Product
from flask_jwt_extended import jwt_required

#blueprint for product related routes
product_blueprint = Blueprint('products', __name__)

# Get all products
@product_blueprint.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }
        output.append(product_data)
    return jsonify(output), 200

# Get a product by ID
@product_blueprint.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product_by_id(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description
    }), 200

# Create new product
@product_blueprint.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price'],
        description=data['description']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created", "product": {
        "id": new_product.id,
        "name": new_product.name,
        "price": new_product.price,
        "description": new_product.description
    }}), 201

# Update product by ID
@product_blueprint.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    data = request.get_json()

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
        db.session.commit()
        return jsonify({
            "message": "Product updated successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description
            }
        }), 200  
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": str(e)}), 500  # Internal server error


# Delete  product by ID
@product_blueprint.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200
