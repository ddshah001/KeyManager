from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.keys import Key, KeySchema
from api.utils.database import db

key_routes = Blueprint("key_routes", __name__)

@key_routes.route('/', methods = ['POST'])
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