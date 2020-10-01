from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.keys import Key, KeySchema
from api.utils.database import db

key_routes = Blueprint("key_routes", __name__)

