from flask import Flask, make_response, request, jsonify, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import Article, User, db

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class ClearSession(Resource):
    def delete(self):
        session.clear()
        return make_response(
            {"message" : "Session cleared"}
        )

class Articles(Resource):
    def get(self):
        articles = [article.to_dict() for article in Article.query.all()]
        response = make_response(
            articles,
            200
        )

        return response

class ShowArticle(Resource):
    def get(self, id):
        article = Article.query.filter(Article.id == id).first()

        if not article:
            return make_response(
                {"error" : f"Article with id {id} not found."},
                404
            )

        if "page_views" in session:
            session["page_views"] = session["page_views"] + 1
        else:
            session["page_views"] = 1


        if session["page_views"] > 3:
            return make_response(
                {"message" : "Maximum pageview limit reached."},
                401
            )

        response = make_response(
            article.to_dict(),
            200
        )
        return response

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")

        if not username:
            return make_response(
                {"error" : "Username is required."},
                400
            )

        user = User.query.filter(User.username == username).first()
        if not user:
            return make_response(
                {"error" : "User not found"},
                404
            )

        session["user_id"] = user.id

        return make_response(
            user.to_dict(),
            200
        )


class Logout(Resource):
    def delete(self):
        session.pop("user_id",None)
        return make_response(
            {"message" : "Logged out successfully."},
            200
        )

class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get("user_id")).first()

        if not user:
            return make_response(
                {"error": "Unauthorized"},
                401
            )

        response = make_response(
            user.to_dict(),
            200
        )

        return response



class MemberOnlyIndex(Resource):
    def get(self):
        user_id = session.get("user_id")

        if not user_id:
            return make_response(
                {"error": "Not authorized"},
                401
            )
        articles = [article.to_dict() for article in Article.query.filter(Article.is_member_only == True).all()]

        return make_response(
            articles,
            200
        )


class MemberOnlyArticle(Resource):
    def get(self, id):
        user_id = session.get("user_id")
        if not user_id:
            return make_response(
                {"error" : "Not authorized"},
                401
            )

        article = Article.query.filter(Article.id == id, is_member_only=True).first()

        if not article:
            return make_response(
                {"error" : f"Article with id {id} not found."}
            )

        return make_response(
            article.to_dict(),
            200
        )



api.add_resource(ClearSession, "/clear")
api.add_resource(Articles, "/articles")
api.add_resource(ShowArticle, "/articles/<int:id>")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")
api.add_resource(MemberOnlyIndex, "/members")
api.add_resource(MemberOnlyArticle, "/members/<int:id>")


if __name__ == "__main__":
    app.run(debug=True, port=5555)
