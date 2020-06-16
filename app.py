from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Class for DB
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False) # this length for hashing
    
# Decorator route
@app.route("/")
def index():
    return render_template("index.html")

# file ➡️ signup.html
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # sha256 for encrypting the password
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        new_user = Users(username=request.form["username"], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        return "You've registered successfully"
        
    return render_template("singup.html")

# file ➡️ login.html
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            return "You are logged in"

        return "Your credentials are invalid, check and try again"
    
    return render_template("login.html")

# file ➡️ index.html
@app.route("/search")
def search():
    nickname = request.args.get("userone")
    user = Users.query.filter_by(username=nickname).first()

    if user: 
        return user.username
    return "The user doesn't exist."

# Extra
@app.route("/about")
def about():
    return "RESTful API with Flask (micro framework)"

if __name__ == "__main__":
    db.create_all()
    app.run(host='127.0.0.1', port=2000, debug=True)