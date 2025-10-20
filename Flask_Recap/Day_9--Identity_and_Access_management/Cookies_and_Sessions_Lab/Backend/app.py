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


class ClearSession(Resource):
    def get(self):
        session.clear()
        return make_response(
            {"message": "200: Successfully cleared session data."},
            200
        )

api.add_resource(ClearSession, "/clear")



class Articles(Resource):
    def get(self):
        articles = [article.to_dict() for article in Article.query.all()]

        response = make_response(
            articles,
            200
        )

        return response

api.add_resource(Articles, "/articles")



class ShowArticle(Resource):
    def get(self, id):
        article = Article.query.filter(Article.id == id).first()

        if not article:
            return make_response(
                {"error" : f"Article with id {id} not found."},
                404
            )

        session['page_views'] = session['page_views'] + 1 if 'page_views' in session else 1

        if session['page_views'] > 3:
            return make_response(
                {"message" : "Maximum pageview limit reached."},
                401
            )

        response = make_response(
            article.to_dict(),
            200
        )

        return response

api.add_resource(ShowArticle,"/articles/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)