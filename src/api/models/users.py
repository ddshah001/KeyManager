from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from api.models.keys import KeySchema
from passlib.hash import sha256_crypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(1024))
    email = db.Column(db.String(128), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    isVerified = db.Column(db.Boolean, nullable=False, default=False)
    keys = db.relationship('Key', backref='User', cascade="all, delete-orphan")

    def __init__(self, name, username, password, email, keys=[]):
        self.name = name
        self.username = username
        self.password = sha256_crypt.hash(password)
        self.email = email
        self.keys = keys
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()

    @staticmethod
    def verify_hash(password,hash):
        return sha256_crypt.verify(password,hash)

class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session
    
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=True)
    created = fields.String(dump_only=True)
    keys = fields.Nested(KeySchema, many=True, only=['name', 'id'])