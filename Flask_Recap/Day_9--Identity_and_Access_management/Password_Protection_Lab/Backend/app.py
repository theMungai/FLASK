from flask_restful import Resource
from flask import request, session, make_response
from config import bcrypt

from models import User
from config import db, api, app

class ClearSession(Resource):
    def delete(self):
        session.clear()

        return make_response(
            {"message" : "Session cleared"},
            200
        )

class SignUp(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if password != password_confirmation:
            return make_response({"error": "Passwords do not match."}, 400)

        if not username or not password:
            return make_response(
                {"error" : "Username and password are required."},
                400
            )

        if User.query.filter(User.username == username).first():
            return make_response(
                {"error" : "Username already taken."},
                400
            )

        new_user = User(username = username)
        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id

        return make_response(
            new_user.to_dict(),
            201
        )

class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get("user_id")).first()

        if not user:
            return make_response(
                {"error" : "Not authorized"},
                401
            )

        return make_response(
            user.to_dict(),
            200
        )

class Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return make_response(
                {"error" : "Username and password required."},
                400
            )

        user = User.query.filter(User.username == username).first()
        if not user:
            return make_response(
                {"error" : "User not found."},
                400
            )

        if not bcrypt.check_password_hash(user._password_hash, password):
            return make_response(
                {"error" : "Invalid password"},
                400
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



api.add_resource(SignUp, "/signup", endpoint="signup")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")


if __name__ == "__main__":
    app.run(port=5555, debug=True)