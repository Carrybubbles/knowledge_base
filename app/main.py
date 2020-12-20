from flask import Flask
from h2o import h2o

app = Flask(__name__)
h2o.init()

@app.route('/ok')
def health():
    return "Hello, World!"

@app.route('/model')
def model():
    return h2o.models()
