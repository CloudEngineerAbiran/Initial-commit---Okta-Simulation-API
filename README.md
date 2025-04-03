# Okta Simulation API

This project is a **Flask-based API** that simulates user provisioning and deprovisioning, similar to how Okta manages user authentication. It includes endpoints to create and delete users while storing them in a local database using SQLAlchemy.

## 📂 Project Structure

```
📦 okta_simulation
├── 📂 routes/             # Contains route handlers (Blueprints)
│   ├── __init__.py       # Makes `routes/` a Python package
│   ├── user_routes.py    # User management API routes
├── app.py                # Main Flask application
├── config.py             # Configuration file (database settings)
├── models.py             # Database models (User schema)
├── requirements.txt      # Dependencies
├── instance/             # Stores SQLite DB (if used)
└── README.md             # Documentation
```

---

## 🚀 Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd okta_simulation
```

### 2️⃣ Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```bash
python3 app.py
```
The API will be available at: **http://127.0.0.1:5000**

---

## 📌 Configuration (`config.py`)
```python
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/users.db'  # SQLite DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

## 📌 Database Model (`models.py`)
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
```

---

## 📌 Main Flask Application (`app.py`)
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    # Import and register the Blueprint
    from user_routes import user_routes
    app.register_blueprint(user_routes)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == "__main__":
    app = create_app()
    print("🚀 Okta Simulation API is running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", debug=True)
```

---

## 📌 API Endpoints (`user_routes.py`)
```python
from flask import Blueprint, request, jsonify
from models import db, User

user_routes = Blueprint("user_routes", __name__)

# Home Route
@user_routes.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Okta Simulation API!"})

# Create User
@user_routes.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "username" not in data or "email" not in data:
        return jsonify({"error": "Missing username or email"}), 400
    
    new_user = User(username=data["username"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "User created successfully!",
        "user": {"id": new_user.id, "username": new_user.username, "email": new_user.email}
    }), 201

# Delete User
@user_routes.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200
```

---

## 📌 API Usage & Testing

### 🔹 Test Home Route
```bash
curl -X GET http://127.0.0.1:5000/
```
#### ✅ Response:
```json
{"message": "Welcome to the Okta Simulation API!"}
```

### 🔹 Create a User
```bash
curl -X POST http://127.0.0.1:5000/users \
     -H "Content-Type: application/json" \
     -d '{"username": "john_doe", "email": "john@example.com"}'
```
#### ✅ Response:
```json
{
    "message": "User created successfully!",
    "user": {"id": 1, "username": "john_doe", "email": "john@example.com"}
}
```

### 🔹 Delete a User
```bash
curl -X DELETE http://127.0.0.1:5000/users/1
```
#### ✅ Response:
```json
{"message": "User deleted successfully!"}
```

---

## 📌 Deployment Guide
### Deploy with Docker
1️⃣ Create a `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]
```

2️⃣ Build and Run:
```bash
docker build -t okta-simulation-api .
docker run -p 5000:5000 okta-simulation-api
```

---

## 📌 License
This project is licensed under the **MIT License**.

---

## 📌 Contribution
Feel free to fork this repository and submit pull requests! 😊




Project Overview
This project is a Flask-based Okta Simulation API that allows user provisioning and deprovisioning. It simulates basic authentication and user management functionalities similar to Okta. The API supports creating users, deleting users, and retrieving API status.

What We Have Done
Project Structure Setup: Organized files into app.py, models.py, config.py, and separate route files.

Database Integration: Used Flask-SQLAlchemy to manage user data.

Blueprint Implementation: Created user_routes.py for handling API endpoints.

Flask Application Initialization: Defined create_app() to initialize Flask and register routes.

Debugging & Deployment: Resolved issues like circular imports, port accessibility, and binding errors.

Usage & Necessity
Why is this Needed?

Helps developers simulate Okta-like user management without needing an actual Okta setup.

Useful for testing authentication workflows before integrating with a real identity provider.

Acts as a lightweight local alternative for managing users in a secure and structured manner.

How to Use It?

Run the Flask app:

bash
Copy
Edit
python3 app.py
Access API in a browser at:

cpp
Copy
Edit
http://127.0.0.1:5000/
API Endpoints:

GET / → Check if the API is running.

POST /users → Create a new user.

DELETE /users/<id> → Delete a user.

