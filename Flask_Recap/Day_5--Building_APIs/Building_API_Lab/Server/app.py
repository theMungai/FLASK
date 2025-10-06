from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc
from flask_restx import Api, Resource

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

api = Api(app, doc='/redoc')

migrate = Migrate(app, db)
db.init_app(app)


@api.route("/")
class Index(Resource):
    def get(self):
        return "<h1>Bakery GET API</h1>"


@api.route("/bakeries")
class Bakeries(Resource):
    def get(self):
        bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]

        response = make_response(
            bakeries,
            200
        )
        return response


@api.route("/bakeries/<int:id>")
class BakeryById(Resource):
    def get(self,id):
        bakery = Bakery.query.filter(Bakery.id == id).first()
        if not bakery:
            return f"Bakery with id {id} was not found"

        response = make_response(
            bakery.to_dict(),
            200
        )
        return response


@api.route("/baked_goods/by_price")
class BakedGoodsByPrice(Resource):
    def get(self):
        baked_goods = [goods.to_dict() for goods in BakedGood.query.order_by(BakedGood.price.desc()).all()]

        response = make_response(
            baked_goods,
            200
        )
        return response


@api.route("/baked_goods/most_expensive")
class MostExpensiveBakedGoods(Resource):
    def get(self):
        most_expensive = BakedGood.query.order_by(desc(BakedGood.price)).limit(1).first()

        response = make_response(
            most_expensive.to_dict(),
            200
        )

        return response


if __name__ == "__main__":
    app.run(debug=True, port=5555)
