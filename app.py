import locale
import pathlib

from flask import Flask
from flask_filter import FlaskFilter
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

import os
from dotenv import load_dotenv
from h2o import h2o

filtr = FlaskFilter()

load_dotenv(os.path.join(pathlib.Path(__file__).parent.parent.absolute(), '.env'))

locale.setlocale(locale.LC_TIME, locale.getlocale())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
swagger = Swagger(app)
db = SQLAlchemy(app)
filtr.init_app(app)

h2o.connect(ip='192.168.0.167', port=54323)

import web.apis
import web.models
