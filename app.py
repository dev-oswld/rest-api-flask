from flask import Flask

app = Flask(__name__)

# Decorator route
@app.route("/")
def index():
    return "Hello World!"

# Extra
@app.route("/about")
def about():
    return "RESTful API with Flask (micro framework)"

# Working with string and int
@app.route("/user/<int:id>/<string:user>")
def username(id, user):
    return "Hello {} the ID is {}".format(user, id)

# And floats 
@app.route("/sum/<float:a>/<float:b>")
@app.route("/sum/")
def sum(a=1, b=2):
    if a is 1:
        return "The default sum is {}".format(a + b)
    else:
        return "The dynamic sum is {}".format(a + b)

if __name__ == "__main__":
    # Auto reloading
    app.run(host='127.0.0.1', port=2000, debug=True)