import os
import pathlib
from h2o import h2o


class Model:
    x = []
    columns = []
    model_name = ''

    def __init__(self, x, columns, model_name):
        self.x = x
        self.columns = columns
        self.model_name = model_name

    def get_frame(self):
        return h2o.H2OFrame(dict(zip(self.columns, self.x)))


class H2oManager:

    def predict(self, model: Model):
        path_to_model = os.path.join(os.path.join(pathlib.Path(__file__).parent.parent.absolute(), 'files'),
                                     model.model_name)
        h2o_model = h2o.load_model(path_to_model)
        return h2o_model.predict(model.get_frame())

    def load_model(self, model_name):
        path_to_model = os.path.join(os.path.join(pathlib.Path(__file__).parent.parent.absolute(), 'files'),
                                     model_name)
        h2o.load_model(path_to_model)

    def get_all_models(self):
        return h2o.models()


h2oManager = H2oManager()
