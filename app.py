import os
from flask import (Flask, escape, flash, g, make_response, redirect,
                   render_template, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from example_bp import example_bp
from requests import get

# Add blueprint
app = Flask(__name__)
app.register_blueprint(example_bp)

# Jinja whitespacing 
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Database
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Class for DB
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False) # this length for hashing
    
@app.before_request
def before_request():
    # A global object
    if "username" in session:
        g.user = session["username"]
    else:
        g.user = None

# Decorator route
@app.route("/")
def index():
    return render_template("index.html")

# file ➡️ index/welcome.html
@app.route("/search")
def search():
    nickname = request.args.get("nickname")
    user = Users.query.filter_by(username=nickname).first()

    if user: 
        status = "how are you?"
        return render_template("welcome.html", status=status, user=user.username)

    return "The user doesn't exist."

# Session - start
@app.route("/home")
def home():
    if g.user:
        return "hi, you are %s" % g.user

    return "You must log in first"

# file ➡️ signup.html
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # sha256 for encrypting the password
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        new_user = Users(username=request.form["username"], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("You've registered successfully", "success") # Message

        return redirect(url_for("login"))
        
    return render_template("singup.html")

# file ➡️ login.html
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            session["username"] = user.username
            return "You are logged in"
        flash("Your credentials are invalid, check and try again", "warning")

    return render_template("login.html")

# Session expire - end
@app.route("/logout")
def logout():
    session.pop("username", None)

    return "You are logged out"

# Cookies
@app.route("/cookie/set")
def set_cookie():
    resp = make_response(render_template("index.html"))
    # Params set cookie: name/value
    resp.set_cookie("uservalue", "dev-oswld")

    return resp

@app.route("/cookie/read")
def read_cookie():
    username = request.cookies.get("uservalue", None)
    if username == None:
        return "The cookie doesn't exist"

    return username

@app.route("/info")
def show_info():
     info = get("http://localhost:2020/api/info").json()
     return render_template("info.html", info=info)

# Extra
@app.route("/about")
def about():
    return redirect("https://github.com/dev-oswld")

# not secure yet, example
app.secret_key = "secret"

if __name__ == "__main__":
    db.create_all()
    app.run(host='127.0.0.1', port=2000, debug=True)
