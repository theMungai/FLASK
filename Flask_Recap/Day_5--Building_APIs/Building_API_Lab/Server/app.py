from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery,BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def index():
    return "<h1>Bakery GET API</h1>"

@app.route("/bakeries")
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]

    response = make_response(
        bakeries,
        200
    )

    return response

@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if not bakery:
        return f"Bakery with id {id} was not found"

    response = make_response(
        bakery.to_dict(),
        200
    )

    return response

@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    baked_goods = [goods.to_dict() for goods in BakedGood.query.order_by(BakedGood.price.desc()).all()]

    response = make_response(
        baked_goods,
        200
    )
    return response

@app.route("/baked_goods/most_expensive")
def most_expensive_baked_goods():
    most_expensive = BakedGood.query.order_by(desc(BakedGood.price)).limit(1).first()

    response = make_response(
        most_expensive.to_dict(),
        200
    )
    return response



if __name__ == "__main__":
    app.run(debug=True, port=5555)