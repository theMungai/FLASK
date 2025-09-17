from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    response_body = {"message" : "Flask SQLAlchemy Lab 1"}
    return make_response(response_body,200)


@app.route("/earthquakes/<int:id>")
def filter_by_id(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        found_data  = {
            "id" : earthquake.id,
            "magnitude" : earthquake.magnitude,
            "location" : earthquake.location,
            "year" : earthquake.year
        }

        return jsonify(found_data),200
    else:
        return jsonify({
            "message": f"Earthquake {id} was not found."
        }),404

@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_earthquake_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quake_list = [
        {
            "id" : quake.id,
            "magnitude" : quake.magnitude,
            "location" : quake.location,
            "year" : quake.year
        }
        for quake in quakes
    ]

    return jsonify({
        "count" : len(quake_list),
        "quakes" : quake_list
    })




if __name__ == "__main__":
    app.run(port=5555, debug=True)