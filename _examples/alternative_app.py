'''
About this:
Show in console/browser (localhost) the request.
'''

from flask import Flask, jsonify
import requests

app = Flask(__name__)
request_status = ""

# REST API public
host = "https://jsonplaceholder.typicode.com"

# GET
@app.route("/get-posts", methods=["GET"])
def get_posts():
    r = requests.get(host + "/posts")
    for p in r.json():
        post = "userId: {}\nid: {}\nTitle: {}\nPost: {}\n\n".format(
            p["userId"], p["id"], p["title"], p["body"])
        print(post)
    
    # All post
    return "Yeah, it´s works"


# POST
@app.route("/add-post", methods=["POST"])
def add_post():
    userId = 11
    title = "Esto es en español"
    body = "Más texto escrito en español para variar el contenido"

    # See more => https://en.wikipedia.org/wiki/Payload_(computing)
    # The part of transmitted data, related to headers and metadata
    payload = {"userId": userId, "title": title, "body": body}
    r = requests.post(host + "/posts", json=payload)

    p = r.json()
    post = "userId: {}\nid: {}\nTitle: {}\nPost: {}\n\n".format(
        p["userId"], p["id"], p["title"], p["body"])
    print("\nNew post")
    print(post)

    return "Yeah, yeah"


# PUT
@app.route("/edit-post", methods=["PUT"])
def edit_post():
    id = 100
    userId = 10
    title = "Tengo más contenido en español por hacer"
    body = "Aquí debe de haber mucho texto en español"

    payload = {"userId": userId, "title": title, "body": body}
    r = requests.put(host + "/posts/" + id, json=payload)

    p = r.json()
    post = "userId: {}\nid: {}\nTitle: {}\nPost: {}\n\n".format(
        p["userId"], p["id"], p["title"], p["body"])

    print("\nHere is the post")
    print(post)

    return "Ok ok"


# DELETE
@app.route("/delete-post", methods=["DELETE"])
def delete_post():
    id = 100

    r = requests.delete(host + "/posts/" + id)

    print(r.json())
    print("The post was deleted")

    return "okey"


# Star here
@app.route("/")
def index():
    return "Request status ➡️ " + request_status

# 1
@app.before_request
def before_request():
    global request_status
    request_status += " Before request 🚩 "
    # print("Before request")

# 2
@app.after_request
def after_request(response):
    global request_status
    request_status = request_status + " After request 🚩 "
    # print("After request")

    return response

# 3
@app.teardown_request
def teardown_request(response):
    global request_status
    request_status = request_status + " Teardown request 🚩 "
    # print("Teardown request")

    return response

@app.route("/api/info")
def show_info():
    return "REST API"

if __name__ == "__main__":
    app.run(port=2020, debug=True)
