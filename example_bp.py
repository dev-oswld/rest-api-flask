# See more here => https://realpython.com/flask-blueprint/
from flask import Blueprint

example_bp = Blueprint("example_bp", __name__)

@example_bp.route("/element/blueprint")
def index():
    return "This is an example with bp"