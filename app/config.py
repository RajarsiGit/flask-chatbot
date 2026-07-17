import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

    CHATBOT_NAME = os.environ.get("CHATBOT_NAME", "Chatterbot")
    CHATBOT_DATABASE_URI = os.environ.get(
        "CHATBOT_DATABASE_URI", "sqlite:///database.sqlite3"
    )
