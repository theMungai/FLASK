from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API"
        }

        response = make_response(
            response_dict,
            200
        )

        return response


api.add_resource(Home, "/")

class Newsletters(Resource):
    def get(self):
        newsletters = [newsletter.to_dict() for newsletter in Newsletter.query.all()]

        response = make_response(
            newsletters,
            200
        )

        return response

    def post(self):
        data = request.get_json()
        new_record = Newsletter(
            title = data.get("title"),
            body = data.get("body")
        )

        db.session.add(new_record)
        db.session.commit()

        new_record_dict = new_record.to_dict()

        response = make_response(
            new_record_dict,
            201
        )

        return response

api.add_resource(Newsletters, "/newsletters")

class NewsletterById(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter(Newsletter.id == id).first()

        if not newsletter:
            return make_response(
                {"error" : f"Newsletter with id {id} not found."},
                404
            )

        response = make_response(
            newsletter.to_dict(),
            200
        )

        return response

    def patch(self, id):
        newsletter = Newsletter.query.filter(Newsletter.id == id).first()

        if not newsletter:
            return make_response(
                {"error" : f"Newsletter with id {id} not found."},
                404
            )

        data = request.get_json()

        for attr, value in data.items():
            setattr(newsletter, attr, value)

        db.session.commit()

        newsletter_dict = newsletter.to_dict()

        response = make_response(
            newsletter_dict,
            200
        )

        return response

    def delete(self, id):
        newsletter = Newsletter.query.filter(Newsletter.id == id).first()

        if not newsletter:
            return make_response(
                {"error" : f"Newsletter with id {id} not found."},
                404
            )

        db.session.delete(newsletter)
        db.session.commit()

        response = make_response(
            {"message" : "Newsletter has been deleted successfully."},
            200
        )

        return response


api.add_resource(NewsletterById, "/newsletters/<int:id>")


if __name__ == "__main__":
    app.run(debug=True, port=5555)