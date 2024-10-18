from flask import session, jsonify
from functools import wraps

# Custom login required decorator for API
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:  # Check if the user is logged in
            return jsonify({"error": "Unauthorized access. Please log in."}), 401  # Return a JSON response with an error
        return f(*args, **kwargs)
    return decorated_function