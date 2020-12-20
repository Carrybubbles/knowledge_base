from flask import Flask

app = Flask(__name__)

@app.route('/ok')
def index():
    return "Hello, World!"