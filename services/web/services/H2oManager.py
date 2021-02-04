import os
import pathlib
from h2o import h2o


class Model:
    x_names = []
    x_values = []
    uuid = ''

    def __init__(self, x_values, x_names, uuid):
        self.x_values = x_values
        self.x_names = x_names
        self.uuid = uuid

    def get_frame(self):
        return h2o.H2OFrame(dict(zip(self.x_names, self.x_values)))


class H2oManager:

    def predict(self, model: Model):
        path = os.environ.get('MODELS_DIR')
        path_to_model = os.path.join(path,
                                     model.uuid)
        h2o_model = h2o.load_model(path_to_model)
        return h2o_model.predict(model.get_frame())

h2oManager = H2oManager()
