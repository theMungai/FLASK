from flask import Flask
from werkzeug.utils import redirect

app = Flask(__name__)

@app.route('/')
def index():
    return "This is my home page."

@app.route('/dodge')
def dodge():
    return redirect("https://www.dodge.com/")

if __name__ == "__main__":
    app.run(debug=True)