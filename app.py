import os
from flask import (Flask, escape, flash, g, make_response, redirect,
                   render_template, request, session, url_for, send_from_directory)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from example_bp import example_bp
from requests import get

# Add blueprint
app = Flask(__name__)
app.register_blueprint(example_bp)

# Jinja whitespacing 
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Upload files
UPLOAD_FOLDER = os.path.abspath("./uploads")
ALLOWED_EXTENSIONS = set(["png", "jpg"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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


# Function to allowed files
def allowed_file(filename):
    # Loop and split the extension 
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_request
def before_request():
    # A global object
    if "username" in session:
        g.user = session["username"]
    else:
        g.user = None

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

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

'''
@app.route("/info")
def show_info():
     info = get("http://localhost:2020/api/info").json()
     return render_template("info.html", info=info)
'''

@app.route("/uploads", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if not "file" in request.files:
            return "No file part in the form"
        f = request.files["file"]

        # Without extension 
        if f.filename == "":
            return "No file selected"
        
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            # Specific folder
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("get_file", filename = filename))
        return "File not allowed"


    # Backend to frontend, little example
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Upload File</title>
    </head>
    <body>
        <h2>Upload File</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <br>
            <input type="submit" value="Upload">
        </form>
    </body>
    </html>"""

# Dynamic route
# Important use < >
@app.route("/uploads/<filename>")
def get_file(filename):
    # Flask function
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Extra
@app.route("/about")
def about():
    return redirect("https://github.com/dev-oswld")

# not secure yet, example
app.secret_key = "secret"

if __name__ == "__main__":
    db.create_all()
    app.run(host='127.0.0.1', port=2000, debug=True)
