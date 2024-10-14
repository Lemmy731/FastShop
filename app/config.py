import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'fastshop.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
