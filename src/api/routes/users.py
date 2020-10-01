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

@user_routes.route('/', methods = ['GET'])
def get_user_list():
    users_data = User.query.all()
    user_schema = UserSchema(many=True, only=['name', 'username', 'email', 'id'])
    users = user_schema.dump(users_data)
    return response_with(resp.SUCCESS_200, value={"users": users})

@user_routes.route('/<int:user_id>', methods = ['GET'] )
def get_user_details(user_id):
    user_data = User.query.get_or_404(user_id)
    user_schema = UserSchema()
    user = user_schema.dump(user_data)
    return response_with(resp.SUCCESS_200, value={"user": user})

@user_routes.route('/<int:user_id>', methods = ['PUT'])
def update_user_details(user_id):
    data = request.get_json()
    get_user = User.query.get_or_404(user_id)
    get_user.name = data['name']
    get_user.email = data['email']
    #db.session.add(get_user)
    db.session.commit()
    user_schema = UserSchema()
    user = user_schema.dump(get_user)
    return response_with(resp.SUCCESS_200, value={"user":user})

@user_routes.route('/<int:user_id>', methods = ['DELETE'])
def delete_user(user_id):
    get_user = User.query.get_or_404(user_id)
    db.session.delete(get_user)
    db.session.commit()
    return response_with(resp.SUCCESS_204)


