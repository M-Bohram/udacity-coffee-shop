import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth, get_token_auth_header

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()


# ROUTES
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    formatted_drinks = [drink.short() for drink in drinks]
    return jsonify({"success": True, "drinks": formatted_drinks})


@app.route('/drinks-detail')
@requires_auth(permission='get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()
    formatted_drinks = [drink.long() for drink in drinks]
    return jsonify({"success": True, "drinks": formatted_drinks})


@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def add_drink(payload):
    if 'title' not in request.get_json() or 'recipe' not in request.get_json():
        abort(400)
    title = request.get_json()['title']
    recipe = request.get_json()['recipe']
    if type(recipe) is dict:
        recipe_list = []
        recipe_list.append(recipe)
        recipe_str = json.dumps(recipe_list)
    else:
        recipe_str = json.dumps(recipe)
    drink = Drink(title=title, recipe=recipe_str)
    drink.insert()
    formatted_drink = drink.long()
    return jsonify({"success": True, "drinks": formatted_drink})


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def update_drink(payload, id):
    if not Drink.query.get(id):
        abort(404)
    drink = Drink.query.get(id)
    db_title = drink.title
    db_recipe = [{'name': r['name'], 'color': r['color'],
                  'parts': r['parts']} for r in json.loads(drink.recipe)]
    isChanged = False
    if 'title' in request.get_json():
        title = request.get_json()['title']
        if db_title != title:
            drink.title = title
            isChanged = True
    if 'recipe' in request.get_json():
        recipe = request.get_json()['recipe']
        recipe_str = json.dumps(recipe)
        if db_recipe != recipe_str:
            drink.recipe = recipe_str
            isChanged = True
    if isChanged:
        drink.update()
    formatted_drink = drink.long()
    drinks_arr = []
    drinks_arr.append(formatted_drink)
    return jsonify({"success": True, "drinks": drinks_arr})


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(payload, id):
    if not Drink.query.get(id):
        abort(404)
    drink = Drink.query.get(id)
    drink.delete()
    return jsonify({"success": True, "delete": id})

# Error Handling


@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "bad_request"
                    }), 400


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "not_found"
                    }), 404


@app.errorhandler(AuthError)
def unprocessable(error):
    error_info = error.error
    status_code = error.status_code
    return jsonify({
                    "success": False,
                    "error": status_code,
                    "message": error_info['description']
                    }), status_code
