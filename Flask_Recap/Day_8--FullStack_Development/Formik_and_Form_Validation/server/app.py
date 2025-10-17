from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Customer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Customers(Resource):
    def get(self):
        customers = [customer.to_dict() for customer in Customer.query.all()]

        response = make_response(
            customers,
            200
        )

        return response

    def post(self):
        data = request.get_json()
        new_customer = Customer(
            name = data.get("name"),
            age = data.get("age"),
            email = data.get("email")
        )

        db.session.add(new_customer)
        db.session.commit()

        response = make_response(
            new_customer.to_dict(),
            201
        )

        return response

api.add_resource(Customers, "/customers")


if __name__ == "__main__":
    app.run(port=5555, debug=True)