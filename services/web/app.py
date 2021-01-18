# import json
#
# from flask import Flask, request, jsonify
# from h2o import h2o
# from werkzeug.utils import secure_filename
# from H2oManager import h2oManager
# from H2oManager import Model
# from flask_sqlalchemy import SQLAlchemy
# from dbManager import dbManager
#
# import os
# import pathlib
#
# app = Flask(__name__)
# # db = SQLAlchemy(app)
#
# # h2o.connect(ip="h2o", port=54321)
# h2o.init()
#
# @app.route('/ok')
# def health():
#     return "Hello, World!"
#
#
# @app.route('/model/<model_name>', methods=['POST', 'GET', 'DELETE'])
# def model():
#     if request.method == 'GET':
#         return "ok"
#     elif request.method == 'POST':
#         content = json.loads(request.json)
#         model_name = content["modelName"]
#         x = content["x"]
#         y = content["y"]
#
#     else:
#         # delete model
#         return "ok"
#
#
# @app.route('/upload-model', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         resp = jsonify({'message': 'No file part in the request'})
#         resp.status_code = 400
#         return resp
#     file = request.files['file']
#     if file.filename == '':
#         resp = jsonify({'message': 'No file selected for uploading'})
#         resp.status_code = 400
#         return resp
#     #проверка на то что файл есть
#     if file:
#         filename = secure_filename(file.filename)
#         path = os.path.join(pathlib.Path(__file__).parent.absolute(), 'files')
#         file.save(os.path.join(path, filename))
#         h2oManager.load_model(filename)
#         resp = jsonify({'message': 'File successfully uploaded'})
#         resp.status_code = 201
#         return resp
#     else:
#         resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
#         resp.status_code = 400
#         return resp
#
#
# @app.route('/models', methods=['GET'])
# def models():
#     models = h2oManager.get_all_models()
#     resp = jsonify(models)
#     resp.status_code = 200
#     return resp
#
#
# @app.route('/predict/<model_name>', methods=['POST'])
# def predict_model(model_name):
#     content = json.loads(request.json)
#     x = content['x']
#     column_names = content['column_names']
#     model = Model(x, column_names, model_name)
#     result = h2oManager.predict(model)
#     print(result['predict'][0])
#     resp = jsonify({'message': "asd"})
#     resp.status_code = 200
#     return resp
#
#
# @app.route('/predicts', methods=['POST'])
# def predict_models():
#     return "ok"
#
# if __name__ == '__main__':
#     app.run()

# -*- coding: utf-8 -*-
import locale
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

locale.setlocale(locale.LC_TIME, locale.getlocale())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost:5432/knowledge_base'


db = SQLAlchemy(app)

import models
import apis