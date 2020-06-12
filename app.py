from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Class for DB
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    
# Decorator route
@app.route("/")
def index():
    title = "A title with emoji 👌"
    list = ["i", "love", "python"]
    return render_template("index.html", title=title, list=list)

# Insert method
@app.route("/insert/default")
def insert_default():
    new_post = Posts(title="Default title")
    db.session.add(new_post)
    db.session.commit()
    return "The post was created"

# Select method
@app.route("/select/default")
def select_default():
    post = Posts.query.filter_by(id=1).first()
    print(post.title)
    return "Query done, look the console"

# Extra
@app.route("/about")
def about():
    return "RESTful API with Flask (micro framework)"

if __name__ == "__main__":
    db.create_all()
    app.run(host='127.0.0.1', port=2000, debug=True)