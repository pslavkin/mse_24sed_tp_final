#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 21:44:24 2019

@author: glavigna
"""

import datetime
import time
from influxdb import InfluxDBClient
import psutil


# Set up a client for InfluxDB
dbclient = InfluxDBClient('192.168.0.21', 8086, 'root', 'root', 'sed')

while(True):
    receiveTime=datetime.datetime.utcnow()
    cpu_percent_float = psutil.cpu_percent()
    json_body = [
        {
            "measurement": "bbb_cpu_load",
            "time": receiveTime,
            "fields": {
            "value": cpu_percent_float
            }
        }
    ]
    print("Uso de CPU: " + str(cpu_percent_float))
    print("Finished writing to InfluxDB")
    dbclient.write_points(json_body)
    time.sleep(0.5)


