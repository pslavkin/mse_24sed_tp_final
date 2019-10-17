#import paho.mqtt.client as mqtt
import datetime
import time
from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

dbclient = InfluxDBClient('localhost', 8086, 'root', 'root', 'demo')

client = mqtt.Client()
client.on_publish = on_publish
client.on_connect = on_connect


connOK=False
while(connOK == False):
    try:
        client.connect("dci.ddns.net", 1883, 60)
        connOK = True
    except:
        connOK = False
    time.sleep(2)

while(True):
    result = dbclient.query('SELECT "value" FROM "mote1/rssi"  WHERE time > now() - 1m')
    points = list(result.get_points())
    print(str(datetime.datetime.now()) + " : " + str(len(points)))
    client.publish("mote1/rssi_rate",len(points)) 
    if(len(points)== 0):
        client.publish("mote1/rssi_alarm",1) 
    else:
        client.publish("mote1/rssi_alarm",0) 
    time.sleep(5)
    