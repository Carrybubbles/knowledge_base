from app import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AIModel(db.Model):
    
    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    uuid = db.Column(db.String)
    description = db.Column(db.String)
    file = db.Column(db.LargeBinary)
    x = db.Column(db.ARRAY(db.String))
    y = db.Column(db.String)
    metrics = db.Column(db.JSON)

    def __init__(self, category=None, uuid=None, description=None, file=None, x=None ,y=None , metrics=None):
        self.category = category
        self.uuid = uuid,
        self.description = description
        self.file = file
        self.x = x
        self.y = y
        self.metrics = metrics

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if getattr(self, c.name) is not None}