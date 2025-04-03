from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # ✅ Import Blueprint from the correct location
    from user_routes import user_routes

    # ✅ Register Blueprint
    app.register_blueprint(user_routes)

    # ✅ Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    print("🚀 Okta Simulation API is running on http://127.0.0.1:8080")

    # ✅ Run Flask on port 8080 instead of 5000
    app.run(host="127.0.0.1", port=8080, debug=True)

