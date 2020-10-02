from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.keys import Key, KeySchema
from api.utils.database import db
from flask_jwt_extended import jwt_required

key_routes = Blueprint("key_routes", __name__)

@key_routes.route('/', methods = ['POST'])
@jwt_required
def create_key():
    try:
        data = request.get_json()
        key_schema = KeySchema()
        key = key_schema.load(data)
        result = key_schema.dump(key.create())
        return response_with(resp.SUCCESS_201, value={"key":result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

@key_routes.route('/',methods=['GET'])
@jwt_required
def get_key_list():
    key_data = Key.query.all()
    key_schema = KeySchema(many=True, only=['id', 'name', 'user_id'])
    keys = key_schema.dump(key_data)
    return response_with(resp.SUCCESS_200, value={'keys': keys})

@key_routes.route('/<int:id>', methods = ['PUT'])
@jwt_required
def update_key(id):
    data = request.get_json()
    get_key = Key.query.get_or_404(id)
    get_key.name = data['name']
    get_key.data = data['data']
    db.session.commit()
    key_schema = KeySchema()
    key = KeySchema.dump(get_key)
    return response_with(resp.SUCCESS_200, value={'key':key})

@key_routes.route('/<int:id>', methods = ['DELETE'])
@jwt_required
def delete_key(id):
    get_key = Key.query.get_or_404(id)
    db.session.delete(get_key)
    db.session.commit()
    return response_with(resp.SUCCESS_204)



