from flask import Blueprint, current_app, render_template, request

bp = Blueprint("chat", __name__)


@bp.route("/")
def home():
    return render_template("index.html")


@bp.route("/get")
def get_bot_response():
    user_text = request.args.get("msg", "")
    bot = current_app.extensions["chatbot"]
    return str(bot.get_response(user_text))
