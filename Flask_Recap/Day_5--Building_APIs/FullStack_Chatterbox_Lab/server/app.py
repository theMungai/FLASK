from flask import Flask, make_response, jsonify, request
from flask_cors import  CORS
from flask_migrate import Migrate
from flask_restx import Api, Resource

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

api = Api(app, doc='/docs')

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)


@api.route('/')
class Home(Resource):
    def get(self):
        return "<h1>Welcome to Chatterbox</h1>"

@api.route("/messages")
class Messages(Resource):
    def get(self):
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at.desc()).all()]

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

        message_dict = new_message.to_dict()

        response = make_response(
            jsonify(message_dict),
            200
        )

        return response

@api.route("/messages/<int:id>")
class MessagesById(Resource):
    def get(self, id):
        message = Message.query.filter(Message.id == id).first()

        if not message:
            return make_response(
                {"Error" : f"Message with id {id} not found."},
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
                {"Error": f"Message with id {id} not found."},
                400
            )

        data = request.get_json()

        for attr, value in data.items():
            setattr(message, attr, value)

        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
            jsonify(message_dict),
            200
        )

        return response


    def delete(self, id):
        message = Message.query.filter(Message.id == id).first()

        if not message:
            return make_response(
                {"Error" : f"Message with id {id} not found."},
                400
            )
        db.session.delete(message)
        db.session.commit()

        response = make_response(
            {"message" : "Message deleted successfully"},
            200
        )

        return response

if __name__ == "__main__":
    app.run(port=5555, debug=True)
