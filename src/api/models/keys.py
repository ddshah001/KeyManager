from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class Key(db.Model):
    __tablename__ = 'keys'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    data = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, data, user_id=None):
        self.name = name
        self.data = data
        self.user_id = user_id
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class KeySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Key
        sqla_session = db.session
    
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    data = fields.String(required=True)
    user_id = fields.Integer()