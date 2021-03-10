from datetime import date, datetime

from sqlalchemy.sql import expression

from app import db
from web.models.AIModel import AIModel, Metric


class DbManager:

    def insert_model(self,
                     uuid=None,
                     file=None):
        metric = Metric()
        today = datetime.now()
        model = AIModel(
            uuid=uuid,
            file=file,
            creation_time=today,
            metric=metric)
        db.session.add(model)
        db.session.commit()

    def update_model(self,
                     category=None,
                     uuid=None,
                     author=None,
                     description=None,
                     creation_time=None,
                     variant=None,
                     task=None,
                     filename=None,
                     is_full_to_train=True,
                     maxf1=None,
                     x=None,
                     y=None,
                     hash_data_train=None,
                     hash_data_test=None,
                     task_type=None,
                     r2=None,
                     mse=None,
                     rmse=None,
                     additional=None):
        model = AIModel.query.filter_by(uuid=uuid).first()
        if model is None:
            raise
        model.category = category
        model.description = description
        model.x = x
        model.y = y
        model.updated = datetime.now()
        model.author = author
        model.hash_data_train = hash_data_train
        model.hash_data_test = hash_data_test
        model.task_type = task_type
        model.creation_time = creation_time
        model.variant = variant
        model.task = task
        model.filename = filename
        if is_full_to_train is True:
            model.is_full_to_train = expression.true()
        else:
            model.is_full_to_train = expression.false()
        model.metric.maxf1 = maxf1
        model.metric.mse = mse
        model.metric.rmse = rmse
        model.metric.r2 = r2
        model.metric.additional = additional

        db.session.add(model)
        db.session.commit()

    def model_exist(self, ruuid):
        return db.session.query(db.exists().where(AIModel.uuid == ruuid)).scalar() is True

    def get_model(self, ruuid, hasFile=False):
        aiModel = db.session.query(AIModel).filter_by(uuid=ruuid).first()

        aiModel.id = None
        if not hasFile:
            aiModel.file = None
            aiModel.uuid = None

        return aiModel

    def delete_model(self, ruuid):
        db.session.query(AIModel).filter_by(uuid=ruuid).delete()
        db.session.commit()

    def get_models(self):
        return db.session.query(AIModel.metrics).all()


dbManager = DbManager()
