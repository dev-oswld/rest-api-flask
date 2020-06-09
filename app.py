from flask import Flask

app = Flask(__name__)

# Decorator route
@app.route("/")
def index():
    return "Hello World!"

# Extra
@app.route("/about")
def about():
    return "Rest API with Flask (micro-framework)"

if __name__ == "__main__":
    app.run()

