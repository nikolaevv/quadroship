import os

basedir = os.path.abspath(os.path.dirname(__file__))

#UPLOAD_FOLDER = 'photos'
speed = 40
max_flight_time = 10

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False