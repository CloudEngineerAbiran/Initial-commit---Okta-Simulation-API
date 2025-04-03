from flask import Blueprint, request, jsonify
from models import db, User

user_routes = Blueprint("user_routes", __name__)

# Test Route
@user_routes.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Okta Simulation API!"})


# Provision a New User
@user_routes.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()

        # Input Validation
        if not data or "username" not in data or "email" not in data:
            return jsonify({"error": "Missing required fields: username or email"}), 400

        # Check for existing user
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 409

        # Create new user
        new_user = User(username=data["username"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User created successfully!",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get All Users
@user_routes.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        return jsonify({"users": user_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get a Single User by ID
@user_routes.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": {"id": user.id, "username": user.username, "email": user.email}}), 200


# Deprovision (Delete) a User
@user_routes.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

