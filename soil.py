# -*- coding: utf-8 -*-
# @Time : 12/22/2021 14:28
# @Author : wxy
# @File : soil.py
# @Software: PyCharm
import os
import pymongo
# Read, edit and write soil files
def get_soil( para, lon_in, lat_in):
    cli = pymongo.MongoClient('127.0.0.1',27017)
    db = cli['soil_properties']
    coll = db[para]
    datas = coll.find({'geometry': {'$near': {
        "coordinates": [
            lon_in,
            lat_in
        ],
        "type": "Point"}, '$maxDistance': 1000}})[0]
    # z=[]
    for i in range(len(datas[para])):
        if str(datas[para][i])=='nan':
            datas[para][i]=datas[para][i-1]

    return datas[para][:6]