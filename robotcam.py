# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 21:55:37 2019

@author: waiho
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 10:47:09 2019

"""
import paho.mqtt.client as paho
#import paho.mqtt.publish as publish
import picamera
import time
import base64
from threading import Thread
#import json

broker = "10.12.108.241"
port = 1883
keepalive = 60
#keepalive: maximum period in seconds allowed between communications with the broker. 
#If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker

###### define callbacks ################################################################  

#def convert_msg_to_json(): 
#    #initialize the sender dictionary     
#    broker_out = {"broker1":"169.254.51.214","Flame":flame_msg, 
#                  "Pot":pot_msg, "Gas": gas_msg, "Flow rate":flowrate_msg}
#    #encode the data as a json string    
#    data_out= json.dumps(broker_out)    
#    return data_out

#the callback for when a message has been sent to the broker
def on_publish(client, userdata, mid):
    print("Published to topic: " + str(mid) + "\n")
    pass

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc) + "\n")
    pass

def on_disconnect(client, userdata, rc):
    if rc!=0:
        print("Unexpected disconnection")
    pass
def capture_plant(tier):
    with picamera.PiCamera() as cam :
        cam.resolution=(640,480)
        cam.capture('vfarm/%d.jpg' % (tier))
        print("Captured tray"+str(tier))

#instantiate an object of the mqtt client
client = paho.Client("rpi_sub", clean_session= False, userdata=None) 

#assign the functions to the respective callbacks 
client.on_publish= on_publish
client.on_connect= on_connect
client.on_disconnect= on_disconnect

client.username_pw_set("pgharvest", "1234")

client.reconnect_delay_set(min_delay=1, max_delay=180)

#establish connection to the broker
client.connect(broker, port, keepalive)

def capture():
    for tier in range(1,5,1):
            start=time.time()
            capture_plant(tier)
            f=open('vfarm/%d.jpg' % (tier), "rb")
            byteArray=base64.b64encode(f.read())
            client.publish('vfarm/%d' % (tier), byteArray)
            time.sleep(1)

threadA = Thread(target = client.loop_start())
threadB = Thread(target = capture())

threadA.run()
threadB.run()

#publish the payload on the defined MQTT topic
#arguments:
#topic
#payload: Passing an int or float will result in the payload being converted to a string representing that number. 
#If you wish to send a true int/float, use struct.pack() to create the payload you require
#qos: quality of service level to use 
#client.publish("dev/test2", convert_msg_to_json())

####################### INTEGRATE VARIABLES USED IN COMBINED SENSOR SCRIPT BELOW ##################################
#publish multiple messages to a broker then disconnect cleanly
#msgs= [{"topic":"rpi2/sensor/flame", "payload":str(flame_msg), "qos":1, "retain":True},
#       {"topic":"rpi2/sensor/pot", "payload":str(pot_msg), "qos":1, "retain":True},
#       {"topic":"rpi2/sensor/gas", "payload":str(gas_msg), "qos":1, "retain":True},
#       {"topic":"rpi2/sensor/flowrate", "payload":str(flowrate_msg), "qos":1, "retain":True}]
#publish.multiple(msgs, hostname=broker, port=port, keepalive=keepalive)


#the blocking call that processes network traffic, dispatches callbacks and handles automatic reconnecting        
