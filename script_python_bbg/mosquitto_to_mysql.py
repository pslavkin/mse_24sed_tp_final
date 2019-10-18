#!/usr/bin/python3
import pymysql
import paho.mqtt.client as mqtt
import time

topic_dict = {
        "mote1/rssi"	:["mote1_rssi"		,0,"mote1_alive"],
        "mote2/rssi"	:["mote2_rssi"		,0,"mote2_alive"],
        "mote2/imu_temp":["mote2_imu_temp"	,0,""		],
        }

mydb       = pymysql.connect(
  host     = "localhost",
  user     = "bbb",
  passwd   = "1234",
  database = "bbb"
)
mycursor = mydb.cursor()

def on_connect(client, userdata, flags, rc):
	print("Connected with result code {}".format(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
#	client.subscribe  ("$SYS/#")
	client.subscribe  ( "mote1/rssi" )
	client.subscribe  ( "mote2/rssi" )
	client.subscribe  ( "mote2/imu_temp" )
	
def on_disconnect(client, userdata, rc):
	print("Disconnection!!")
	print("vuelvo a conectar")
	client.reconnect()



def database(topic,value):
	search=topic_dict.get(topic,"")
	t=search[0]
	if(t!=""):
		save2Mysql(t,value)
		if search[2]!="":
			search[1]=0 #reset tout


def on_log(client, userdata, level, buf):
    print("log: ",buf)

def on_message(client, userdata, message):
	msg=str(message.payload.decode("utf-8"))
	print("Topic= {} msg= {}".format(message.topic,msg))
	#    print("message topic="       ,message.opic)
	#    print("message qos="         ,message.qos)
	#    print("message retain flag=" ,message.retain)
	database(message.topic,msg)

client            = mqtt.Client (  )
client.connect      ( "localhost", keepalive=3600 )
client.on_log     = on_log
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.loop_start (          )

def save2Mysql(table,data):
	mycursor.execute("INSERT INTO  {} VALUES ({},NULL)".format(table,data))
	mydb.commit()
	print("mysql table {} value {}".format(table,data))

disconnect=0
while 1 :

	client.loop()
	for key in topic_dict:
		if(topic_dict[key][2]!=""):
			print("time out {} {}".format(topic_dict[key][0],topic_dict[key][1]))
			save2Mysql(topic_dict[key][2],topic_dict[key][1])
			topic_dict[key][1]+=1
			if(topic_dict[key][1]>60):
				disconnect=1
	if disconnect==1:
		disconnect=0
		print("desconecto x timeout")
		for key in topic_dict:
			topic_dict[key][1]=0	
		client.disconnect()
	time.sleep(1)

print("salio del main")
client.loop_stop()
client.disconnect()


