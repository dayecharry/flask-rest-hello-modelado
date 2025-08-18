"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Owner, Pet, Doctor
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ------------- PET ---------
# seleccionar todas las mascotas


@app.route("/pets", methods=["GET"])
def get_all_pets():
    pets = Pet.query.all()  # SQL --> SELECT * FROM pet
    return jsonify([pet.serialize() for pet in pets]), 200

# Seleccionar  mascota por id


@app.route("/pet/<int:pet_id>",  methods=["GET"])
def get_pet_id(pet_id):
    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({"error": "El id no existe"}), 404
    return jsonify(pet.serialize()), 200

# Crear una nueva mascota


@app.route("/pet", methods=["POST"])
def create_pet():
    data = request.get_json()
    name = data.get("name")
    weight = data.get("weight")
    race = data.get("race")

    if not (name or weight or race):
        return jsonify({"error": "Campos oblogatorios"}), 400

    #clave = valor--> propiedadBD = VieneFront
    pet = Pet(name=name, weight=weight,race=race)
    db.session.add(pet)
    db.session.commit()
    return jsonify({"message": "Agregado con exito"}), 201

@app.route("/pet/<int:pet_id>", methods=["PUT"])
def modify_pet(pet_id): # pet_id --> se envia en la url
    pet = Pet.query.get(pet_id) 
    if not pet:
        return jsonify({"error": "El id no existe"}), 404
    data= request.get_json()  # se envia en el body 
    if "name" in data:
        pet.name = data["name"] # data.get("name")
    if "weight" in data:
        pet.weight = data["weight"]
    db.session.commit()
    return jsonify({"message": "Modificado con exito"}), 200


@app.route("/pet/<int:pet_id>", methods=["DELETE"])
def delete_pet(pet_id): # pet_id --> se envia en la url
    pet = Pet.query.get(pet_id) 
    if not pet:
        return jsonify({"error": "El id no existe"}), 404
    db.session.delete(pet)
    db.session.commit()

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
