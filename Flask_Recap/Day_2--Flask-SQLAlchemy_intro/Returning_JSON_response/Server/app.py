from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.dp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False   #to display each key/value pair on a separate line

migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)



@app.route("/demo_json")
def demo_json():
    pet = Pet.query.first()
    pet_dict = {
        'id': pet.id, 
        'name': pet.name, 
        'species':pet.species
    }
    return make_response(pet_dict,200)

# when a dictionary is passed into [make_response()], Flask automatically transforms the dictionary into JSON by calling a method named [jsonify()].


@app.route("/pets/<int:id>")
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        body = {
            "id" : pet.id,
            "name" : pet.name,
            "species" : pet.species
        }
        status = 200
    else:
        body = {"message" : f"Pet {id} not found."}
        status = 404

    return make_response(body, status)



@app.route("/pets/<string:species>")
def pet_by_species(species):
    pets = []
    for pet in Pet.query.filter_by(species = species).all():
        pet_dict = {
            "id" : pet.id,
            "name" : pet.name
        }
        pets.append(pet_dict)
    body = {
        "count" : len(pets),
        "pets" : pets
    }
    return make_response(body, 200)




if __name__ == "__main__":
    app.run(port=5555, debug=True)