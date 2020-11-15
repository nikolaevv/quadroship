# -*- coding: utf8 -*-

from flask import Flask, render_template, send_from_directory, session, redirect, url_for, escape, request, Response
from flask_sqlalchemy import SQLAlchemy
from app import models, app, db
from flask_api import status
import os
from config import speed, max_flight_time, power_station_lon, power_station_lat, t_up
import numpy as np
import base64
import datetime
import requests
import json
import time
from math import pi, sin, cos, asin, sqrt, ceil

import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('server.crt', 'server.key')
from flask_cors import CORS, cross_origin
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


earth_r = 6371
# Усредённное значение радиуса Земли

def convert_to_radians(degrees):
    return degrees * (pi / 180)

def eval_time(lat1, lon1, lat2, lon2):
    lat1, lon1 = convert_to_radians(lat1), convert_to_radians(lon1)
    lat2, lon2 = convert_to_radians(lat2), convert_to_radians(lon2)
    # Конвертация в радианы

    d = 2 * earth_r * asin(sqrt(sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * (sin((lon2 - lon1) / 2) ** 2 )))
    t = ceil(d / speed * 60) + t_up
    # Расчёт времени доставки от A в B

    return [d, t]

def check_data(data, requireds):
    if type(data) == dict:
        for required_param in requireds:
            if data.get(required_param, None) is None:
                return False
        return True
    return False

def queryset_to_list(queryset):
    flat_list = []
    for q in queryset:
        q_dict = q.__dict__
        del q_dict['_sa_instance_state']
        #del q_dict['date_create']

        flat_list.append(q_dict)
    return flat_list

def get_queadro_coords():
    # Заглушка
    return 56.717021, 37.155946

def check_available(lat1, lon1, lat2, lon2, power_level = 100):
    lat0, lon0 = get_queadro_coords()
    t = eval_time(lat0, lon0, lat1, lon1)[1] + eval_time(lat1, lon1, lat2, lon2)[1] + eval_time(lat2, lon2, power_station_lat, power_station_lon)[1]
    return (max_flight_time*power_level/100) - t > 2

@app.route('/api/available/check', methods = ['POST'])
def get_available():
    requireds = ('sendLat', 'sendLon', 'recvLat', 'recvLon')
    if request.get_json() is not None:
        if check_data(request.get_json(), requireds) is True:
            return {'available': check_available(request.get_json()['sendLat'], request.get_json()['sendLon'], request.get_json()['recvLat'], request.get_json()['recvLon'], 100)}
        return 'Some data is missing', status.HTTP_400_BAD_REQUEST
    return 'Some data is missing', status.HTTP_400_BAD_REQUEST

@app.route('/api/order/get', methods = ['GET'])
def get_active_order():
    if request.args.get('vk_id', None) is not None:
        vk_id = request.args.get('vk_id')
        orders = queryset_to_list(models.Order.query.filter((models.Order.sender == vk_id) | (models.Order.receiver == vk_id)).filter(models.Order.status != 0).all())

        if len(orders) > 0:
            print(orders[0])
            return json.dumps(orders[0])
        return None
    return 'Some params are missing', status.HTTP_400_BAD_REQUEST

@app.route('/api/order/create', methods = ['POST'])
def create_order():
    requireds = ('sender', 'receiver', 'sendLat', 'sendLon', 'recvLat', 'recvLon', 'comment')
    if request.get_json() is not None:
        if check_data(request.get_json(), requireds) is True:
            geo = eval_time(request.get_json()['sendLat'], request.get_json()['sendLon'], request.get_json()['recvLat'], request.get_json()['recvLon'])

            if len(models.Order.query.filter(models.Order.status != 0).all()) == 0 and check_available(request.get_json()['sendLat'], request.get_json()['sendLon'], request.get_json()['recvLat'], request.get_json()['recvLon'], 100):
            
                new_order = models.Order(sender = request.get_json()['sender'],
                                         receiver = request.get_json()['receiver'], 
                                         sendLat = request.get_json()['sendLat'], 
                                         sendLon = request.get_json()['sendLon'], 
                                         recvLat = request.get_json()['recvLat'], 
                                         recvLon = request.get_json()['recvLon'],
                                         comment = request.get_json()['comment'],
                                         status = 1,
                                         way = geo[0],
                                         minutes = geo[1],
                                         date_create = datetime.datetime.now()
                )

                db.session.add(new_order)
                db.session.commit()

                return json.dumps(new_order)
            return 'Quadrocoapter is busy or way is too long', status.HTTP_403_FORBIDDEN
        return 'Some data is missing', status.HTTP_400_BAD_REQUEST
    return 'Some data is missing', status.HTTP_400_BAD_REQUEST

@app.route('/api/order/changestatus', methods = ['POST'])
def change_status():
    requireds = ('id', 'status')
    if request.get_json() is not None:
        if check_data(request.get_json(), requireds) is True:
            orders = models.Order.query.filter(models.Order.id == request.get_json()['id']).all()
            if len(orders) > 0:
                order = orders[0]
                order.status = request.get_json()['status']
                db.session.commit()

                return {}
            return 'Order is not found', status.HTTP_400_BAD_REQUEST
        return 'Some params are missing', status.HTTP_400_BAD_REQUEST
    return 'Some params are missing', status.HTTP_400_BAD_REQUEST

app.secret_key = os.urandom(24)
app.run(host = '0.0.0.0', port = '8000', debug = True, ssl_context=context)
#print(eval_time(56.355642, 37.526208, 56.355147, 37.530657))