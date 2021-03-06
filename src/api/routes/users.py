from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.users import User, UserSchema
from api.utils.database import db
from flask_jwt_extended import create_access_token, jwt_required
from api.utils.token import generate_verification_token, confirm_verification_token
from api.utils.email import send_email
from flask import url_for, render_template_string

user_routes = Blueprint("user_routes", __name__)

@user_routes.route('/', methods = ['POST'])
def create_user():
    try:
        data = request.get_json()
        if(User.find_by_email(data['email']) is not None or User.find_by_username(data['username']) is not None):
            return response_with(resp.INVALID_INPUT_422)
        user_schema = UserSchema()
        user = user_schema.load(data)
        token = generate_verification_token(data['email'])
        verification_email_url = url_for('user_routes.verify_email', token=token, _external=True)
        html = render_template_string("<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p> <p><a href='{{ verification_email }}'>{{ verification_email }}</a></p> <br> <p>Thanks!</p>",verification_email=verification_email_url)
        subject = "Please Verify your email [KeyManager]"
        send_email(user.email, subject, html)
        result = user_schema.dump(user.create())
        return response_with(resp.SUCCESS_201, value={"user":result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

@user_routes.route('/confirm/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except:
        return response_with(resp.SERVER_ERROR_500)
    user = User.query.filter_by(email=email).first_or_404()
    if user.isVerified:
        return response_with(resp.INVALID_INPUT_422)
    else:
        user.isVerified = True
        db.session.commit()
        return response_with(resp.SUCCESS_200, value={'message':'E-mail verified, you can proceed to login now.'})

@user_routes.route('/', methods = ['GET'])
@jwt_required
def get_user_list():
    users_data = User.query.all()
    user_schema = UserSchema(many=True, only=['name', 'username', 'email', 'id'])
    users = user_schema.dump(users_data)
    return response_with(resp.SUCCESS_200, value={"users": users})

@user_routes.route('/<int:user_id>', methods = ['GET'] )
@jwt_required
def get_user_details(user_id):
    user_data = User.query.get_or_404(user_id)
    user_schema = UserSchema()
    user = user_schema.dump(user_data)
    return response_with(resp.SUCCESS_200, value={"user": user})

@user_routes.route('/<int:user_id>', methods = ['PUT'])
@jwt_required
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
@jwt_required
def delete_user(user_id):
    get_user = User.query.get_or_404(user_id)
    db.session.delete(get_user)
    db.session.commit()
    return response_with(resp.SUCCESS_204)

@user_routes.route('/login', methods = ['POST'])
def user_login():
    try:
        data = request.get_json()
        #current_user = User.find_by_username(data['username'])
        if data.get('email'):
            current_user = User.find_by_email(data['email'])
        elif data.get('username'):
            current_user = User.find_by_username(data['username'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if current_user and not current_user.isVerified:
            return response_with(resp.BAD_REQUEST_400)
        if User.verify_hash(data['password'],current_user.password):
            token = create_access_token(identity=current_user.username)
            return response_with(resp.SUCCESS_201, value={'message': 'Logged in as {}'.format(current_user.username), "access_token": token})
        else:
            return response_with(resp.UNAUTHORIZED_403)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)




