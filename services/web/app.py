import locale
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

locale.setlocale(locale.LC_TIME, locale.getlocale())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost:5432/knowledge_base'
swagger = Swagger(app)

db = SQLAlchemy(app)

import apis
import models