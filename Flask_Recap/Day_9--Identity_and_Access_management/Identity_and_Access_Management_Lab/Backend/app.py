from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import db, app, api, bcrypt
from models import User, Recipe

class SignUp(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")
        image_url = data.get("image_url") or data.get("imageUrl")
        bio = data.get("bio")

        if password != password_confirmation:
            return make_response(
                {"error" : "Password do not match"},
                400
            )

        if not username or not password:
            return make_response(
                {"error" : "Username and password required"},
                400
            )

        if User.query.filter(User.username == username).first():
            return make_response(
                {"error" : "Username already taken."},
                400
            )

        new_user = User(
            username = username,
            bio = bio,
            image_url = image_url
        )
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
                {"error": "Username and password required."},
                400
            )

        user = User.query.filter(User.username == username).first()
        if not user:
            return make_response(
                {"error" : "User not found"},
                404
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
            204
        )

class RecipeIndex(Resource):
    def get(self):
        user_id = session.get("user_id")

        if not user_id:
            return make_response(
                {"error" : "Not authorized"},
                401
            )

        recipes = [recipe.to_dict() for recipe in Recipe.query.all()]

        return make_response(
            recipes,
            200
        )


    def post(self):
        user_id = session.get("user_id")

        if not user_id:
            return make_response(
                {"error" : "Not authorized"},
                401
            )

        data = request.get_json()
        title=data.get("title")
        instructions=data.get("instructions")
        minutes_to_complete=data.get("minutes_to_complete")

        if not title or not instructions or minutes_to_complete is None:
            return make_response(
                {"error" : "All fields (title, instructions, minutes_to_complete) are required"},
                422
            )

        try:
            new_recipe = Recipe(
                title = title,
                instructions = instructions,
                minutes_to_complete = minutes_to_complete,
                user_id = user_id
            )

            db.session.add(new_recipe)
            db.session.commit()

            return make_response(
                new_recipe.to_dict(),
                201
            )

        except Exception as error:
            db.session.rollback()
            return make_response(
                {"error" : f"Unprocessable Entity: {str(error)}"},
                422
            )



api.add_resource(SignUp, "/signup", endpoint="signup")
api.add_resource(CheckSession, "/check_session", endpoint="check_session" )
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(RecipeIndex, "/recipes", endpoint="recipes")


if __name__ == "__main__":
    app.run(port=5555, debug=True)