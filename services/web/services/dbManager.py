from app import app, db
from models.AIModel import AIModel

class DbManager:

    def insert_model(self, model_name, x, y, uuid, desc):
        model = AIModel(model_name=model_name, x=x, y=y, uuid=uuid, description=desc)
        db.session.add(model)
        db.session.commit()

    def model_exist(self, ruuid):
        return db.session.query(db.exists().where(AIModel.uuid == ruuid)).scalar() is True

    def get_model(self, ruuid):
        return db.session.query(AIModel).filter_by(uuid= ruuid).first()

    def delete_model(self, ruuid):
        db.session.query(AIModel).filter_by(uuid=ruuid).delete()
        db.session.commit()

    def get_models(self):
        return db.session.query(AIModel).all()

dbManager = DbManager()