from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flasgger import Swagger

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
swagger = Swagger(app)

class Home(Resource):
    def get(self):
        return '<h1>Welcome to Chatterbox FullStack app.</h1>'

api.add_resource(Home, '/')

class Messages(Resource):
    def get(self):
        messages = [message.to_dict() for message in Message.query.all()]

        response = make_response(
            messages,
            200
        )

        return response

    def post(self):
        data = request.get_json()

        new_message = Message(
            body = data.get("body"),
            username = data.get("username")
        )

        db.session.add(new_message)
        db.session.commit()

        response = make_response(
            new_message.to_dict(),
            201
        )

        return response

api.add_resource(Messages, "/messages")


class MessageById(Resource):
    def get(self, id):
        message = Message.query.filter(Message.id == id).first()

        if not message:
            return make_response(
                {"error" : f"Message with id {id} not found."},
                404
            )

        response = make_response(
            message.to_dict(),
            200
        )

        return response

    def patch(self, id):
        message = Message.query.filter(Message.id == id).first()

        if not message:
            return make_response(
                {'error' : f'message with id {id} not found.'},
                404
            )

        data = request.get_json()

        for attr, value in data.items():
            setattr(message, attr, value)

        db.session.commit()

        response = make_response(
            message.to_dict(),
            200
        )

        return response

    def delete(self, id):
        message = Message.query.filter(Message.id == id).first()

        if not message:
            return make_response(
                {"error" : f"Message with id {id} not found."},
                404
            )

        db.session.delete(message)
        db.session.commit()

        response = make_response(
            {"message" : "Message deleted successfully."},
            200
        )

        return response

api.add_resource(MessageById, "/messages/<int:id>")



if __name__ == "__main__":
    app.run(debug=True, port=5555)