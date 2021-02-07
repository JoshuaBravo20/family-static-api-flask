"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['ENV'] = 'development'
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
@app.route('/member', methods=['POST'])
@app.route('/member/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def handle_hello(id = None):

    if request.method == 'GET':       
        if id == None:
            familia = jackson_family.get_all_members()
            return jsonify(familia), 200
        if id:
            member = jackson_family.get_member(id)
            return jsonify(member), 200

    if request.method == 'POST':

        id = request.json.get("id")
        first_name = request.json.get("first_name")
        last_name = "Jackson"
        age = request.json.get("age")
        lucky_numbers = request.json.get("lucky_numbers")

        if not first_name:
            return jsonify({"msg": "no first_name received, please type it in"}), 400
        if not age:
            return jsonify({"msg": "no age received, please type it in"}), 400
        if not lucky_numbers:
            return jsonify({"msg": "no lucky_numbers received, please type them in"}), 400

        newMember = {
            "first_name": first_name,
            "age": age,
            "lucky_numbers": lucky_numbers
        }

        jackson_family.add_member(newMember)
        return jsonify({"success": "member has been created!"}), 200

    if request.method == 'PUT':

        member = jackson_family.get_member(id)

        first_name = request.json.get("first_name")
        last_name = "Jackson"
        age = request.json.get("age")
        lucky_numbers = request.json.get("lucky_numbers")

        if not first_name:
            return jsonify({"msg": "no first_name received, please type it in"}), 400
        if not age:
            return jsonify({"msg": "no age received, please type it in"}), 400
        if not lucky_numbers:
            return jsonify({"msg": "no lucky_numbers received, please type them in"}), 400

        member["first_name"] = first_name
        member["age"] = age
        member["lucky_numbers"] = lucky_numbers

        return jsonify({"success": "member has been edited!"}), 200

    if request.method == 'DELETE':
        member = jackson_family.get_member(id)
        if not member: 
            return jsonify({"error": "member does not exist!"}), 400
        else:
            jackson_family.delete_member(id)
            return jsonify({"done": True}), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
