from marshmallow import Schema, fields, post_dump

from app import db

class AIModel(db.Model):
    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    uuid = db.Column(db.String)
    author = db.Column(db.String)
    updated = db.Column(db.Date)
    description = db.Column(db.String)
    file = db.Column(db.LargeBinary)
    x = db.Column(db.ARRAY(db.String))
    y = db.Column(db.String)
    hash_data_train = db.Column(db.String)
    hash_data_test = db.Column(db.String)
    task_type = db.Column(db.String)
    metric_id = db.Column(db.Integer, db.ForeignKey('metric.id'))
    metric = db.relationship("Metric", backref=db.backref("AIModel", uselist=False))

    def __init__(self,
                 category=None,
                 uuid=None,
                 author=None,
                 updated=None,
                 description=None,
                 file=None,
                 x=None,
                 y=None,
                 hash_data_train=None,
                 hash_data_test=None,
                 task_type=None,
                 metric=None):
        self.category = category
        self.uuid = uuid,
        self.author = author,
        self.updated = updated,
        self.description = description
        self.file = file
        self.x = x
        self.y = y
        self.hash_data_train = hash_data_train,
        self.hash_data_test = hash_data_test,
        self.task_type = task_type
        self.metric = metric

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if getattr(self, c.name) is not None}

class Metric(db.Model):
    __tablename__ = 'metric'
    id = db.Column(db.Integer, primary_key=True)
    r2 = db.Column(db.String)
    mse = db.Column(db.Numeric)
    rmse = db.Column(db.Numeric)
    additional = db.Column(db.JSON)

    def __init__(self,
                 r2=None,
                 mse=None,
                 rmse=None,
                 additional=None):
        self.r2 = r2
        self.mse = mse,
        self.rmse = rmse,
        self.additional = additional

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if getattr(self, c.name) is not None}


class BaseSchema(Schema):
    SKIP_VALUES = None

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if value is not None
        }

class AIModelSchema(BaseSchema):
    id = fields.Integer()
    category = fields.String()
    uuid = fields.String()
    author = fields.String()
    description = fields.String()
    x = fields.List(fields.String())
    y = fields.String()
    hash_data_train = fields.String()
    hash_data_test = fields.String()
    task_type = fields.String()
    metric = fields.Nested("MetricSchema")

class MetricSchema(BaseSchema):
    r2 = fields.Float()
    mse = fields.Float()
    rmse = fields.Float()
    additional = fields.Dict()

