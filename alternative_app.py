'''
About this:
Example of before, after and teardown request, comming soon in the app.py
Show in console/browser (localhost) the request.
'''

from flask import Flask

app = Flask(__name__)
request_status = ""

# Star here
@app.route("/")
def index():
    return "Request status ➡️ " + request_status

# Global keyword that allows a user to modify a variable outside of the current scope. 
# 1
@app.before_request
def before_request():
    global request_status

    request_status += " Before request"
    print("Before request.")

# 2
@app.after_request
def after_request(response):
    global request_status
    request_status = request_status + " After request "
    print("After request")

    return response

# 3
@app.teardown_request
def teardown_request(response):
    global request_status
    request_status = request_status + " Teardown request "
    print("Teardown request.")

    return response

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=2020, debug=True)
