from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]

        response = make_response(
            plants,
            200
        )

        return response


    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name = data.get("name"),
            image = data.get("image"),
            price = data.get("price")
        )

        db.session.add(new_plant)
        db.session.commit()

        new_plant_dict = new_plant.to_dict()

        response = make_response(
            new_plant_dict,
            200
        )

        return response

api.add_resource(Plants, "/plants")


class PlantById(Resource):
    def get(self, id):
        plant_dict = Plant.query.filter(Plant.id == id).first().to_dict()

        response = make_response(
            plant_dict,
            200
        )

        return response

    def patch(self, id):
        plant = Plant.query.filter(Plant.id == id).first()

        if not plant:
            return make_response(
                {"error" : f"Plant with id {id} not found."},
                404
            )

        data = request.get_json()

        for attr, value in data.items():
            setattr(plant, attr, value)

        db.session.commit()

        plant_dict = plant.to_dict()

        response = make_response(
            plant_dict,
            200
        )

        return response

    def delete(self, id):
        plant = Plant.query.filter(Plant.id == id).first()

        if not plant:
            return make_response(
                {"error" : f"Plant with id {id} not found."},
                404
            )

        db.session.delete(plant)
        db.session.commit()

        response = make_response(
            {"message" : "Plant deleted successfully."},
            200
        )

        return response


api.add_resource(PlantById, "/plants/<int:id>")


if __name__ == "__main__":
    app.run(debug=True, port=5555)