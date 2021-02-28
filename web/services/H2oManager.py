import os
from pathlib import Path

from h2o import h2o

from ..models.AIModel import AIModel


class RequestModel:
    x_names = []
    x_values = []

    def __init__(self, x_values, x_names):
        self.x_values = x_values
        self.x_names = x_names

    def get_frame(self):
        return h2o.H2OFrame(dict(zip(self.x_names, self.x_values)))


class H2oManager:

    def predict(self, request: RequestModel, modelAI: AIModel):
        parent = os.path.join(Path(__file__).parents[2], "models")
        path = os.path.join(parent, modelAI.uuid)
        f = None
        h2oModel = None
        try:
            f = open(path, "w+b")
            f.write(modelAI.file)
            h2oModel = h2o.load_model(path)
            f.close()
            os.remove(path)
        except:
            os.remove(path)
            f.close()
            raise Exception
        return h2oModel.predict(request.get_frame())

    def check_model(self, model, uuid):
        parent = os.path.join(Path(__file__).parents[2], "models")
        path = os.path.join(parent, uuid)
        f = None
        try:
            f = open(path, "w+b")
            f.write(model)
            h2o.load_model(path)
            f.close()
            os.remove(path)
            return True
        except:
            os.remove(path)
            f.close()
            return False

h2oManager = H2oManager()
