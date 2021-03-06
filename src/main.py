import logging
import os
import sys
from flask import Flask
from flask import jsonify
from api.config.config import DevelopmentConfig, TestingConfig, ProductionConfig
from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
from api.routes.users import user_routes
from api.routes.keys import key_routes
from flask_jwt_extended import JWTManager
from api.utils.email import mail


app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)
app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(key_routes, url_prefix='/api/keys')

@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)

@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)

db.init_app(app)
jwt = JWTManager(app)
mail.init_app(app)
with app.app_context():
    db.create_all()

logging.basicConfig(stream=sys.stdout,format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',level=logging.DEBUG)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)