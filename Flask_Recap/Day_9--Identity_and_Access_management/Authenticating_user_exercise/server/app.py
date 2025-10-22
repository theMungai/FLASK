from flask import Flask, make_response, request, session, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")

        if not username:
            return make_response(
                {"error" : "Username is required"},
                400
            )

        user = User.query.filter(User.username == username).first()

        if not user:
            return make_response(
                {"error" : "User not found."},
                404
            )

        session["user_id"] = user.id

        return make_response(
            user.to_dict(),
            200
        )

class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)

        return make_response(
            {"message": "Logged out successfully"},
            200
        )


class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get("user_id")).first()

        if not user:
            return make_response(
                {"error" : "Not Authorized"},
                401
            )

        return make_response(
            user.to_dict(),
            200
        )



api.add_resource(CheckSession, "/check_session")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")


if __name__ == "__main__":
    app.run(debug=True, port=5555)