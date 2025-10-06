from flask import Flask, make_response,request
from flask_migrate import Migrate
from flask_restx import Api, Resource

from models import db, Game, Review, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

api = Api(app, doc='/docs')

migrate = Migrate(app, db)
db.init_app(app)

@api.route("/")
class Index(Resource):
    def get(self):
        return "Index for Game/Review/User API"

@api.route("/games")
class Games(Resource):
    def get(self):
        games = [game.to_dict() for game in Game.query.all()]

        response = make_response(
            games,
            200
        )
        return response

@api.route("/games/<int:id>")
class GameById(Resource):
    def get(self, id):
        game = Game.query.filter(Game.id == id).first()
        game_dict = game.to_dict()

        response = make_response(
            game_dict,
            200
        )
        return response

@api.route("/reviews")
class Reviews(Resource):
    def get(self):
        reviews = [review.to_dict() for review in Review.query.all()]

        response = make_response(
            reviews,
            200
        )

        return response


    def post(self):
        new_review = Review(
            score = request.form.get("score"),
            comment = request.form.get("comment"),
            game_id = request.form.get("game_id"),
            user_id = request.form.get("user_id")
        )
        db.session.add(new_review)
        db.session.commit()

        review_dict = new_review.to_dict()

        response = make_response(
            review_dict,
            201
        )

        return response


@api.route("/reviews/<int:id>")
class ReviewsById(Resource):
    def get(self,id):
        review = Review.query.filter(Review.id == id).first()

        if not review:
            return make_response(
                {"Error":f'Review it id {id} was not found'},
                404
            )

        return make_response(
            review.to_dict(),
            200
        )

    def delete(self, id):
        review = Review.query.filter(Review.id == id).first()

        if not review:
            return make_response(
                {"Error" : f'Review it id {id} was not found'},
                404
            )

        db.session.delete(review)
        db.session.commit()

        response_body = {
            "deleted_successful" : True,
            "message" : "Review deleted."
        }

        return make_response(
            response_body,
            200
        )


    def patch(self, id):
        review = Review.query.filter(Review.id == id).first()
        for attr in request.form:
            setattr(review, attr, request.form.get(attr) )

        db.session.add(review)
        db.session.commit()

        review_dict = review.to_dict()

        response = make_response(
            review_dict,
            200
        )

        return response

@api.route("/users")
class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]

        response = make_response(
            users,
            200
        )

        return response

if __name__ == "__main__":
    app.run(port=5555, debug=True)
