# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 22:09:03 2019

@author: Ian
"""

import paho.mqtt.client as paho
import os
import base64


broker = "localhost"
port = 1883

#keepalive: maximum period in seconds allowed between communications with the broker. 
#If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker
keepalive = 60

#the callback for when the broker has acknowledged the subscription
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic : " + str(mid) + " with Qos " + str(granted_qos) + "/n")
    pass
        
#the callback for when a message has been sent to the broker
def on_publish(client, userdata, mid):
    print("Published to topic: " + str(mid) + "\n")
    pass
    
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc) + "\n")
    pass 

#the callback when the client receives a response to disconnect from the server 
def on_disconnect(client, userdata, rc):
    if rc!=0:
        print("Unexpected disconnection") 
    pass


#the callback for when a PUBLISH message is received from the server
#if payload received matches, execute another command/script
def on_message(client, userdata, msg):
    print("Received message: on topic " + str(msg.topic) 
    + " " + "with QoS " + str(msg.qos))

    #if not os.path.exists(str(msg.topic)):
    #    os.mkdir(str(msg.topic))
        
    """
    save image on local machine under folder vfarm
    """ 
    fh = open(str(msg.topic)+".jpg", "wb") 
    fh.write(base64.b64decode(msg.payload))
    fh.close()    
                   
    print("Image decoded and stored in filepath: "+str(msg.topic))   
    
#################################################################################################################################################################
if __name__ == "__main__":
    #instantiate an object of the mqtt client
    """
    arguments: 1.client_id: the unique client id string used when connecting to the broker        
           2.clean_session: a boolean that determines the client type. 
           If True, the broker will remove all information about this client when it disconnects. 
           If False, the client is a durable client and subscription information and queued messages will be retained when the client disconnects.        
           3.userdata: user defined data of any type that is passed as the userdata parameter to callbacks 
    """
    client = paho.Client("rpi_pub", clean_session= False, userdata=None) 

    #assign the functions to the respective callbacks 
    client.on_publish= on_publish
    client.on_message= on_message
    client.on_connect= on_connect
    client.on_disconnect= on_disconnect

    #set a username and password for broker authentification
    #called before connect*()
    client.username_pw_set("pgharvest", "1234")

    #client.max_inflight_messages.set()

    client.reconnect_delay_set(min_delay=1, max_delay=180)

    #establish connection to the broker
    client.connect(broker, port, keepalive)

    ################################# CLIENT SUBSCRIBES TO CORRESPONDING TOPICS FOR RAW IMAGE DATA ############################
    #subscribe and listen to the specific MQTT topic
    #allows multiple topic subscriptions in a single subscription command
    #on the configuration.yaml file, the corresponding topic for the switch is under command_topic....... to receive image data
    client.subscribe("vfarm/1", 0)
    client.subscribe("vfarm/2", 0)
    client.subscribe("vfarm/3", 0)
    client.subscribe("vfarm/4", 0)
    
    ################################# CLIENT SUBSCRIBES TO CORRESPONDING TOPIC FOR USER VALIDATION ON HARVEST ############################
    """
    client.subscribe("vfarm/switch_tier01_tray01", 0)
    client.subscribe("vfarm/switch_tier01_tray02", 0)
    client.subscribe("vfarm/switch_tier02_tray01", 0)
    client.subscribe("vfarm/switch_tier02_tray02", 0)
    """
    #the blocking call that processes network traffic, dispatches callbacks and handles automatic reconnecting
    client.loop_forever()      