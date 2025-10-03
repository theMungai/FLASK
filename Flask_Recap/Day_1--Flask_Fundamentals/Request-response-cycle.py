import os
from flask import Flask, request, current_app, g, make_response
from requests import session

app=Flask(__name__)

@app.before_request
def app_path():
    g.path = os.path.abspath(os.getcwd())

@app.route("/")
def index():
    host = request.headers.get('host')
    appname = current_app.name
    response_body = f'''
    <h1>The host for this page is {host}</h1>
    <h2>The name of this application is {appname}</h2>
    <h3>The path of this application on the user's device is {g.path}</h3>
    '''
    status_code = 202
    headers = {}
    return make_response(response_body,status_code,headers)


if __name__ == "__main__":
    app.run(port=5555, debug=True)


# Two unique objects that allow us to manipulate request data more effectively
# 1. g -> Is an object that used to store anything that you want to store globally for the lifetime of a request. It is reset with each new request.

# 2. session -> is a dictionary object that can be used to hold onto values between multiple requests.

# URL map -> A dictionary that maps URL.
# Every time we use the @app.route decorator, a new mapping is added to the URL map.

# ============================= REQUEST HOOKS =====================================
# There are 4 types of hooks:
# 1. @app.before_request: runs function before each request
# 2. @app.before_first_request: runs a function before the first request (but not subsequent requests).
# 3. @app.after_request: runs a function after each request
# 4. @app.teardown_request : runs a function after each request, even if an error has occurred.


# An important part of any response is the HTTP status code.


# ============================ SPECIAL RESPONSES ==================================
# 2 cases are most common:
# a) redirect()
# b) abort()