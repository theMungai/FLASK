from flask import Flask

app = Flask(__name__)


# Routing -> The association of URLs and the code that should execute when a request comes in for that URL.
# views -> Functions that map URLs

# "Registration" in Flask means that the view has been connected to the instance of the Flask class.

@app.route("/<string:username>")
def index(username):
    return f'<h1>Welcome to my page!{username} </h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)