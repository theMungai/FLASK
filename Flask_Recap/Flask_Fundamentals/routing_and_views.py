# gunicorn routing_and_views:app

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return '<h1>Python Operations with Flask Routing and Views</h1>'

@app.route("/print/<string:parameter>")
def print_string(parameter):
    print(parameter)
    return parameter


@app.route("/count/<int:parameter>")
def count(parameter):
    result = ""
    for i in range(parameter):
        result += f"{i}\n"
    return result

@app.route("/math/<int:num1>/<operation>/<int:num2>")
def math(num1, operation, num2):
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "div":
        return num1 / num2


# if __name__ == '__main__':
#     app.run( port=5555, debug= )