import os

import uuid
from app import app
from flasgger import swag_from
from flask import request, json, jsonify
from h2o import h2o
from web.services.dbManager import dbManager
from web.services.H2oManager import h2oManager
from web.services.H2oManager import Model

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


@app.route('/model/<uuid>/', methods=['PUT'])
@swag_from('../openapi/put_model.yml')
def put_model(uuid):
    try:
        content = json.dumps(request.json)
        content = json.loads(content)
        metrics = content["metrics"]
        x = content["x"]
        y = content["y"]
        desc = content["description"]
        category = content["category"]
        dbManager.update_model(category=category, metrics=metrics, x=x, y=y, description=desc, uuid=uuid)
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
            id = str(uuid.uuid4())
            dbManager.insert_model(uuid=id, file=file.read())
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
        cur_model.id = None
        cur_model.file = None
        cur_model.uuid = None
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

