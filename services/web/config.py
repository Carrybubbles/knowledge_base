import os

class Config(object):
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:mysecretpassword@localhost:5432/knowledge_base"