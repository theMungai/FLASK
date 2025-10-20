from flask import Flask, make_response, jsonify, request, session
from flask_restful import Api, Resource

app = Flask(__name__)
app.json.compact = False

api = Api(app)

app.secret_key = b'?w\x85Z\x08Q\xbdO\xb8\xa9\xb65Kj\xa9_'

class ShowSession(Resource):
    def get(self, key):

        session["hello"] = session.get("hello") or "World"
        session["goodnight"] = session.get("goodnight") or "Moon"

        response = make_response(jsonify({
            'session' : {
                'session_key': key,
                'session_value' : session[key],
                'session_accessed' : session.accessed
            },
            'cookies' : [{cookie : request.cookies[cookie]} for cookie in request.cookies]
        }), 200)

        response.set_cookie('mouse', 'Cookie')

        return response

api.add_resource(ShowSession, "/sessions/<string:key>")

if __name__ == "__main__":
    app.run(debug=True, port=5555)