from app import app, db
from models.AIModel import AIModel

class DbManager:

    def insert_model(self, category=None, uuid=None, description=None, file=None, x=None, y=None, metrics=None):
        model = AIModel(category=category, uuid=uuid, description=description, file=file, x=x, y=y, metrics=metrics)
        db.session.add(model)
        db.session.commit()

    def update_model(self, category=None, uuid=None, description=None, x=None, y=None, metrics=None):
        model = AIModel.query.filter_by(uuid=uuid).first()
        if model is None:
            raise
        model.category = category
        model.description = description
        model.x = x
        model.y = y
        model.metrics = metrics

        db.session.add(model)
        db.session.commit()

    def model_exist(self, ruuid):
        return db.session.query(db.exists().where(AIModel.uuid == ruuid)).scalar() is True

    def get_model(self, ruuid):
        aiModel = db.session.query(AIModel).filter_by(uuid=ruuid).first()

        aiModel.id = None
        aiModel.file = None
        aiModel.uuid = None

        return aiModel

    def delete_model(self, ruuid):
        db.session.query(AIModel).filter_by(uuid=ruuid).delete()
        db.session.commit()

    def get_models(self):
        return db.session.query(AIModel.metrics).all()

dbManager = DbManager()