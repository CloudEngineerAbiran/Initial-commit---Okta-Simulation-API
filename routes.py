from flask import Blueprint

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/")
def home():
    return "Welcome to the Okta Simulation API!"

