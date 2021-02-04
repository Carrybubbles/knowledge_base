from app import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AIModel(db.Model):

    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String())
    uuid = db.Column(db.String())
    description = db.Column(db.String())
    x = db.Column(db.ARRAY(db.String()))
    y = db.Column(db.String())

    def __init__(self, model_name, x, y, uuid, description):
        self.model_name = model_name
        self.x, = x,
        self.y = y,
        self.uuid = uuid,
        self.description = description

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}