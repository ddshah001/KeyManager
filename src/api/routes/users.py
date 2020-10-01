from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.users import User, UserSchema
from api.utils.database import db

user_routes = Blueprint("user_routes", __name__)

@user_routes.route('/', methods = ['POST'])
def create_user():
    try:
        data = request.get_json()
        user_schema = UserSchema()
        user = user_schema.load(data)
        result = user_schema.dump(user.create())
        return response_with(resp.SUCCESS_201, value={"user":result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)