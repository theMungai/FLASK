from flask  import Flask, make_response,jsonify, request
from flask_migrate import Migrate
from flask_restx import Api, Resource
from sqlalchemy.orm import validates

from models import db, Hero, HeroPower, Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

api = Api(app, doc='/docs')
migrate = Migrate(app, db)
db.init_app(app)

@api.route('/')
class Home(Resource):
    def get(self):
        return "<h1>Welcome to Superheroes</h1>"

@api.route("/heroes")
class Heroes(Resource):
    def get(self):
        heroes = [hero.to_dict() for hero in Hero.query.all()]

        response = make_response(
            heroes,
            200
        )

        return response


@api.route("/heroes/<int:id>")
class HeroesById(Resource):
    def get(self, id):
        hero = Hero.query.filter(Hero.id == id).first()

        if not hero:
            return make_response(
                {"error": f"Hero with id {id} not found"},
                404
            )

        response = make_response(
            hero.to_dict(),
            200
        )

        return response


@api.route("/powers")
class Powers(Resource):
    def get(self):
        powers = [power.to_dict() for power in Power.query.all()]

        response = make_response(
            powers,
            200
        )

        return response

@api.route("/powers/<int:id>")
class PowersById(Resource):
    def get(self, id):
        power = Power.query.filter(Power.id == id).first()

        if not power:
            return make_response(
                {"error" : "Power not found."},
                404
            )

        response = make_response(
            power.to_dict(),
            200
        )

        return response

    @validates('power')
    def validate_description(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Description must be present")
        if len(value.strip()) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value


    def patch(self, id):
        power = Power.query.filter(Power.id == id).first()

        if not power:
            return make_response(
                {"error" : "Power not found."},
                404
            )

        for attr in request.form:
            setattr(power, attr, request.form.get(attr))

        data = request.get_json()

        description = data.get("description")

        errors =[]
        if not description or description.strip() == "":
            errors.append("Description must be present.")
        elif len(description.strip()) < 20:
            errors.append("Description must be at least 20  characters long.")

        if errors:
            return make_response(
                {"errors" : errors},
                422
            )

        power.description = description.strip()

        db.session.commit()


        power_dict = power.to_dict()

        response = make_response(
            power_dict,
            200
        )

        return response


@api.route("/hero_powers")
class HeroPowers(Resource):
    def post(self):
        if not request.is_json:
            return make_response(
                {"error": "Request must be JSON and include 'Content-Type: application/json' header."},
                415
            )

        data = request.get_json()

        strength = data.get("strength")
        power_id = data.get("power_id")
        hero_id = data.get("hero_id")

        errors = []
        allowed_values = ["Strong", "Weak", "Average"]

        if strength not in allowed_values:
            errors.append("Strength must be one of: Strong, Weak, Average")

        if not isinstance(power_id, int):
            errors.append("power_id must be a valid integer.")

        if not isinstance(hero_id, int):
            errors.append("hero_id must be a valid integer.")

        if errors:
            return make_response({"errors": errors}, 400)

        power = Power.query.get(power_id)
        hero = Hero.query.get(hero_id)

        if not power:
            errors.append(f"Power with id {power_id} does not exist.")

        if not hero:
            errors.append(f"Hero with id {hero_id} does not exist.")

        if errors:
            return make_response({"errors": errors}, 404)

        try:
            new_hero_power = HeroPower(
                strength=strength,
                power_id=power_id,
                hero_id=hero_id
            )
            db.session.add(new_hero_power)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return make_response({"errors": [str(e)]}, 400)

        response_data = {
            "id": new_hero_power.id,
            "hero_id": hero.id,
            "power_id": power.id,
            "strength": new_hero_power.strength,
            "hero": {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            },
            "power": {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
        }

        return make_response(response_data, 201)







if __name__ == "__main__":
    app.run(debug=True, port=5555)
