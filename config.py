import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"  # Using SQLite for local testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False

