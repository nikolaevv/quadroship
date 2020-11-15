import os

basedir = os.path.abspath(os.path.dirname(__file__))

#UPLOAD_FOLDER = 'photos'
speed = 40
max_flight_time = 10
power_station_lon = 37.155946
power_station_lat = 56.717021
t_up = 1

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False