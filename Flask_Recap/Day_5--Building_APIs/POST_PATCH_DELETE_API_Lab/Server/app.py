from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restx import Api, Resource
from sqlalchemy.ext.baked import bakery

from models import db, Bakery, BakedGood

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
        return "<h1>Bakery GET-POST-PATCH-DELETE API</h1>"

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
class BakerById(Resource):
    def get(self, id):
        bakery = Bakery.query.filter(Bakery.id == id).first()

        if not bakery:
            return make_response(
                {"Error" : f"Bakery with id {id} not found"},
                404
            )
        response = make_response(
            bakery.to_dict(),
            200
        )

        return response

    def patch(self, id):
        bakery = Bakery.query.filter(Bakery.id == id).first()

        if not bakery:
            return make_response(
                {"Error": f"Bakery with id {id} not found."},
                404
            )

        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))

        db.session.add(bakery)
        db.session.commit()

        bakery_dict = bakery.to_dict()

        response = make_response(
            bakery_dict,
            200
        )

        return response

    def delete(self, id):
        bakery = Bakery.query.filter(Bakery.id == id).first()

        if not bakery:
            return make_response(
                {"Error" : f"Bakery with id {id} not found."},
                404
            )

        db.session.delete(bakery)
        db.session.commit()

        response = make_response(
            {"message" : f"Bakery with id {id} deleted successfully."},
            200
        )

        return response



@api.route("/baked_goods")
class BakedGoods(Resource):
    def post(self):
        new_baked_good = BakedGood(
            name = request.form.get("name"),
            price = request.form.get("price")
        )

        db.session.add(new_baked_good)
        db.session.commit()

        response = make_response(
            {"message" : "Baked good added successfully"},
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
class BakedGoodsMostExpensive(Resource):
    def get(self):
        most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()

        expensive_dict = most_expensive.to_dict()

        response = make_response(
            expensive_dict,
            200
        )

        return response




if __name__ == "__main__":
    app.run(debug=True, port=5555)

