import os
import pathlib

from app import app
from flask import request, json, jsonify
from h2o import h2o
from werkzeug.utils import secure_filename
from services.dbManager import dbManager
from services.H2oManager import h2oManager
from services.H2oManager import Model

# h2o.init()


@app.route('/ok')
def health():
    return "Hello, World!"


@app.route('/model/<model_name>', methods=['POST', 'GET', 'DELETE'])
def model(model_name):
    if request.method == 'GET':
        model = dbManager.get_model(model_name)
        if model is not None:
            resp = jsonify(model.as_dict())
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'message': 'Error. Model with this name doesn\'t consist in knowledge base'})
            resp.status_code = 500
            return resp
    elif request.method == 'POST':
        if dbManager.model_exist(model_name):
            resp = jsonify({'message': 'Error. Model with this name already exist.'})
            resp.status_code = 500
            return resp
        content = json.loads(request.json)
        x = content["x"]
        y = content["y"]
        dbManager.insert_model(model_name=model_name, x=x, y=y)
        resp = jsonify({'message': 'Successfully inserted'})
        resp.status_code = 200
        return resp
    elif request.method == 'DELETE':
        path = os.path.join(pathlib.Path(__file__).parent.parent.absolute(), 'files')
        model_file = os.path.join(path, model_name)
        os.remove(model_file)
        dbManager.delete_model(model_name)
        resp = jsonify({'message': 'Successfully deleted'})
        resp.status_code = 200
        return resp


@app.route('/upload-model', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    # проверка на то что файл есть
    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(pathlib.Path(__file__).parent.absolute(), 'files')
        file.save(os.path.join(path, filename))
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'message': 'Error, check your file'})
        resp.status_code = 400
        return resp


@app.route('/models', methods=['GET'])
def models():
    models = dbManager.get_models()
    result = []
    for cur_model in models:
        result.append(cur_model.as_dict())
    resp = jsonify(result)
    resp.status_code = 200
    return resp


@app.route('/predict/<model_name>', methods=['POST'])
def predict_model(model_name):
    content = json.loads(request.json)
    x = content['x']
    column_names = content['column_names']
    model = Model(x, column_names, model_name)
    result = h2oManager.predict(model)
    value = result.as_data_frame()[1]
    resp = jsonify({'predict': value})
    resp.status_code = 200
    return resp


@app.route('/predicts', methods=['POST'])
def predict_models():
    return "ok"
