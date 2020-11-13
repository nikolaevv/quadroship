# -*- coding: utf8 -*-

from flask import Flask, render_template, send_from_directory, session, redirect, url_for, escape, request, Response
from flask_sqlalchemy import SQLAlchemy
from app import models, app, db
from flask_api import status
import os
import numpy as np
import base64
import datetime
import requests
import json
import time

def queryset_to_list(queryset):
    flat_list = []
    for q in queryset:
        q_dict = q.__dict__
        #del q_dict['_sa_instance_state'] 

        flat_list.append(q_dict)
    return flat_list

@app.route('/api/order/get', methods = ['GET'])
def get_active_order():
    if request.args.get('vk_id', None) is not None:
        vk_id = request.args.get('vk_id')
        orders = queryset_to_list(models.Order.query.filter(models.Order.sender == vk_id).filter(models.Order.status != 0).all())

        if len(orders) > 0:
            return orders[0]
    

app.secret_key = os.urandom(24)
app.run(host='0.0.0.0', port='80', debug=True)