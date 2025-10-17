from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import Movie, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
CORS(app)

api = Api(app)

class Movies(Resource):
    def get(self):
        movies = [movie.to_dict() for movie in Movie.query.all()]

        response = make_response(
            movies,
            200
        )

        return response

api.add_resource(Movies, "/movies")

if __name__ == "__main__":
    app.run(port=5555, debug=True)