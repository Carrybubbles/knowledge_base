from app import app, db
from models.AIModel import AIModel

class DbManager:

    def insert_model(self, model_name, x, y):
        model = AIModel(model_name=model_name, x=x, y=y)
        db.session.add(model)
        db.session.commit()

    def model_exist(self, model_name):
        return db.session.query(db.exists().where(AIModel.model_name == model_name)).scalar() is True

    def get_model(self, name):
        return db.session.query(AIModel).filter_by(model_name= name).first()

    def delete_model(self, name):
        db.session.query(AIModel).filter_by(model_name=name).delete()
        db.session.commit()

    def get_models(self):
        return db.session.query(AIModel).all()

dbManager = DbManager()