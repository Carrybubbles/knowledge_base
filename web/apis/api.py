import os
import uuid

from flasgger import swag_from
from flask import request, json, jsonify

from app import app, filtr
from web.models.AIModel import AIModel
from web.models.AIModel import AIModelSchema
from web.services.H2oManager import RequestModel
from web.services.H2oManager import h2oManager
from web.services.dbManager import dbManager


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
        task_type = content["task_type"]
        if task_type not in ["regression", "classbinary", "classmulticlass"]:
            resp = jsonify({'message': 'select following task_type: regression, classbinary, classmulticlass'})
            resp.status_code = 400
            return resp
        x = content["x"]
        y = content["y"]
        desc = content["description"]
        category = content["category"]
        author = content["author"]
        hash_data_train = content["hash_data_train"]
        hash_data_test = content["hash_data_test"]
        metrics = json.loads(json.dumps(content["metrics"]))
        r2 = metrics["r2"]
        mse = metrics["mse"]
        rmse = metrics["rmse"]
        additional = metrics["additional"]
        dbManager.update_model(category=category,
                               author=author,
                               x=x,
                               y=y,
                               description=desc,
                               uuid=uuid,
                               hash_data_test=hash_data_test,
                               hash_data_train=hash_data_train,
                               task_type=task_type,
                               mse=mse,
                               rmse=rmse,
                               r2=r2,
                               additional=additional)
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
        key = request.headers['key-for-delete']
        if key == os.environ.get('KEY_FOR_DELETE'):
            dbManager.delete_model(uuid)
            resp = jsonify({'message': 'Ok'})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'message': 'You have no permission for this operation'})
            resp.status_code = 403
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
            file = file.read()
            id = str(uuid.uuid4())
            if h2oManager.check_model(file, id):
                dbManager.insert_model(uuid=id, file=file)
                resp = jsonify({'uuid': id})
                resp.status_code = 200
                return resp
            else:
                resp = jsonify({'message': 'Model is not trained by H2O'})
                resp.status_code = 500
                return resp
    except:
        resp = jsonify({'message': 'Internal server error'})
        resp.status_code = 500
        return resp

@app.route('/models', methods=['POST'])
@swag_from('../openapi/get_models.yml')
def models():
    try:
        query = filtr.search(AIModel, request.json.get("filters"), AIModelSchema)
        if query is not None:
            aiModelSchema = AIModelSchema()
            data = aiModelSchema.dumps(query, many=True)
            resp = jsonify()
            resp.data = data
            resp.status_code = 200
        else:
            resp = {}
            resp.status_code = 200
    except:
        resp = jsonify({'message': 'Internal server error'})
        resp.status_code = 500
    return resp


@app.route('/predict/<uuid>', methods=['POST'])
@swag_from('../openapi/post_predict.yml')
def predict_model(uuid):
    try:
        content = json.dumps(request.json)
        content = json.loads(content)
        x = content['x_values']
        column_names = content['x_names']
        requestModel = RequestModel(x, column_names)
        model = dbManager.get_model(uuid, True)
        result = h2oManager.predict(requestModel, model)
        value = result.as_data_frame()[1]
        resp = jsonify({'predict': value})
        resp.status_code = 200
        return resp
    except:
        resp = jsonify({'message': 'Internal server error'})
        resp.status_code = 500
        return resp

