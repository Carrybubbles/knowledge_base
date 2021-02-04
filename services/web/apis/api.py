import os
import pathlib

import uuid
from app import app
from flasgger import swag_from
from flask import request, json, jsonify
from h2o import h2o
from werkzeug.utils import secure_filename
from services.dbManager import dbManager
from services.H2oManager import h2oManager
from services.H2oManager import Model

h2o.connect(ip=os.environ.get('H2O_ADDRESS'), port=os.environ.get('H2O_PORT'))

@app.route('/model/<uuid>/', methods=['GET'])
@swag_from('../openapi/get_model.yml')
def get_model(uuid):
    try:
        model = dbManager.get_model(uuid)
        if model is not None:
            resp = jsonify(model.as_dict())
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({})
            resp.status_code = 200
            return resp
    except:
        resp = jsonify({'message': 'Internal server error'})
        resp.status_code = 500
        return resp


@app.route('/model', methods=['POST'])
@swag_from('../openapi/post_model.yml')
def post_model():
    try:
        content = json.dumps(request.json)
        content = json.loads(content)
        uuid = content["uuid"]
        if dbManager.model_exist(uuid):
            resp = jsonify({'message': 'Forbidden. Model with this guid already exist'})
            resp.status_code = 403
            return resp
        x = content["x"]
        y = content["y"]
        desc = content["description"]
        model_name = content["model_name"]
        dbManager.insert_model(model_name=model_name, x=x, y=y, desc=desc, uuid=uuid)
        resp = jsonify({'message': 'Ok'})
        resp.status_code = 200
        return resp
    except:
        resp = jsonify({'message': 'Internal server error'})
        resp.status_code = 500
        return resp


@app.route('/model/<uuid>/', methods=['DELETE'])
@swag_from('../openapi/delete_model.yml')
def delete_model(uuid):
    try:
        path = os.environ.get('MODELS_DIR')
        model_file = os.path.join(path, uuid)
        os.remove(model_file)
        dbManager.delete_model(uuid)
        resp = jsonify({'message': 'Ok'})
        resp.status_code = 200
        return resp
    except:
        resp = jsonify({'message': 'Internal server error'})
        resp.status_code = 500
        return resp


@app.route('/upload-model', methods=['POST'])
@swag_from('../openapi/post_upload_model.yml')
def upload_file():
    try:
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file:
            path = os.environ.get('MODELS_DIR')
            id = str(uuid.uuid4())
            filename = id
            file.save(os.path.join(path, filename))
            resp = jsonify({'uuid': id})
            resp.status_code = 200
            return resp
    except:
        resp = jsonify({'message': 'Internal server error'})
        resp.status_code = 500
        return resp


@app.route('/models', methods=['GET'])
@swag_from('../openapi/get_models.yml')
def models():
    models = dbManager.get_models()
    result = []
    for cur_model in models:
        result.append(cur_model.as_dict())
    resp = jsonify(result)
    resp.status_code = 200
    return resp


@app.route('/predict/<uuid>', methods=['POST'])
@swag_from('../openapi/post_predict.yml')
def predict_model(uuid):
    content = json.dumps(request.json)
    content = json.loads(content)
    x = content['x_values']
    column_names = content['x_names']
    model = Model(x, column_names, uuid)
    result = h2oManager.predict(model)
    value = result.as_data_frame()[1]
    resp = jsonify({'predict': value})
    resp.status_code = 200
    return resp


@app.route('/predicts', methods=['POST'])
def predict_models():
    return "ok"
