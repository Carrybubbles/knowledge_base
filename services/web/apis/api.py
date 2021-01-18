import os
import pathlib

from app import app
from flask import request, json, jsonify
from werkzeug.utils import secure_filename
from services.dbManager import dbManager
from services.H2oManager import h2oManager

@app.route('/ok')
def health():
    return "Hello, World!"


@app.route('/model/<model_name>', methods=['POST', 'GET', 'DELETE'])
def model(model_name):
    if request.method == 'GET':
        model = dbManager.get_model(model_name)
        if model is not None:
            resp = jsonify(model)
            resp.status_code = 200
            return resp
        else:
            return ('', 200)
    elif request.method == 'POST':
        if dbManager.model_exist(model_name):
            resp = jsonify({'message': 'Error model_name'})
            resp.status_code = 500
            return resp
        content = json.loads(request.json)
        x = content["x"]
        y = content["y"]
        dbManager.insert_model(model_name=model_name, x=x, y=y)
        resp = jsonify({'message': 'Succuss inserted'})
        resp.status_code = 200
        return resp
    else:
        # delete model
        return "ok"


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
    #проверка на то что файл есть
    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(pathlib.Path(__file__).parent.absolute(), 'files')
        file.save(os.path.join(path, filename))
        h2oManager.load_model(filename)
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


@app.route('/models', methods=['GET'])
def models():
    models = h2oManager.get_all_models()
    resp = jsonify(models)
    resp.status_code = 200
    return resp


@app.route('/predict/<model_name>', methods=['POST'])
def predict_model(model_name):
    content = json.loads(request.json)
    x = content['x']
    column_names = content['column_names']
    model = Model(x, column_names, model_name)
    result = h2oManager.predict(model)
    print(result['predict'][0])
    resp = jsonify({'message': "asd"})
    resp.status_code = 200
    return resp


@app.route('/predicts', methods=['POST'])
def predict_models():
    return "ok"