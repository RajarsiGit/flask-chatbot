from flask import Flask

from .chatbot import create_bot
from .config import Config


def create_app(config_object=Config, bot=None):
    app = Flask(__name__)
    app.config.from_object(config_object)

    app.extensions["chatbot"] = bot or create_bot(
        app.config["CHATBOT_NAME"], app.config["CHATBOT_DATABASE_URI"]
    )

    from .routes import bp

    app.register_blueprint(bp)

    return app
