# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 14:24:31 2019

@author: Ian
"""

import paho.mqtt.client as paho
import serial

broker = "10.12.218.81"
port = 1883

#keepalive: maximum period in seconds allowed between communications with the broker. 
#If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker
keepalive = 60

ser = serial.Serial("/dev/ttyACM0", 9600, timeout=0)

#motor_dict = {"tier01_rack01": "turn left, right, up, down",
    #              "tier01_rack02": "turn up, left, right, down",
    #              "tier02_rack01": "turn left, down right, up",
    #              "tier02_rack02": "turn down, left, right, up"}
    
""" ################################### DEFINE FUNCTIONS AND CALLBACKS BELOW ###########################################
"""
          
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
    """
    the callback for when the client receives a CONNACK response from the server
    the value of rc indicates success or not:
        0: Connection successful    
        1: Connection refused - incorrect protocol version 
        2: Connection refused - invalid client identifier 
        3: Connection refused - server unavailable 
        4: Connection refused - bad username or password 
        5: Connection refused - not authorised 
        6-255: Currently unused
    """
    pass 

#the callback when the client receives a response to disconnect from the server 
def on_disconnect(client, userdata, rc):
    if rc!=0:
        print("Unexpected disconnection") 
    pass

def on_message(client, userdata, msg):
    print("Received message: on topic " + str(msg.topic) 
    + " " + "with QoS " + str(msg.qos))
    
    result = msg.payload.decode()
    #result is a dictionary called rack_status
    #rack_status = {"tier01_rack01": "Y",
    #               "tier01_rack02": "Y",
    #               "......",
    #              }
    
    for rack, status in result.items():
        if str(status) == "Y":
            rack_encode = rack.encode()
            ser.write(rack_encode)
            
    #if you want to send an integer, float or double variable, encode it as follows
    #motor_cmd = 5
    #motor_cmd _encode = b'%d' %motor_cmd #change %d based on type of variable

    #if you want to send a string, encode it as follows
    #motor_cmd = "High"
    #motor_cmd_encode = motor_cmd.encode()
    pass


if __name__ == "__main__":
    #instantiate an object of the mqtt client
    """
    arguments: 1.client_id: the unique client id string used when connecting to the broker        
           2.clean_session: a boolean that determines the client type. 
           If True, the broker will remove all information about this client when it disconnects. 
           If False, the client is a durable client and subscription information and queued messages will be retained when the client disconnects.        
           3.userdata: user defined data of any type that is passed as the userdata parameter to callbacks 
    """
    client = paho.Client("rpi_sub", clean_session= False, userdata=None) 

    #assign the functions to the respective callbacks 
    client.on_publish= on_publish
    client.on_message= on_message
    client.on_connect= on_connect
    client.on_disconnect= on_disconnect

    #set a username and password for broker authentification
    #called before connect*()
    #client.username_pw_set("waihong", "1234")

    #client.max_inflight_messages.set()

    client.reconnect_delay_set(min_delay=1, max_delay=180)

    #establish connection to the broker
    client.connect(broker, port, keepalive)

    """
    #SUBSCRIBE to topic:....
    #arguments:1.topic
          2.payload: Passing an int or float will result in the payload being converted to a string representing that number
          If you wish to send a true int/float, use struct.pack() to create the payload you require
          3.qos: quality of service level to use
          4.retain: if set to True, the message will be set as the retained message for the topic 
    """

    ################################# CLIENT SUBSCRIBES TO CORRESPONDING TOPICS FOR RAW IMAGE DATA ############################
    #subscribe and listen to the specific MQTT topic
    #allows multiple topic subscriptions in a single subscription command
    #on the configuration.yaml file, the corresponding topic for the switch is under command_topic....... to receive image data
    client.subscribe("vfarm/motors", 0)
    
    #the blocking call that processes network traffic, dispatches callbacks and handles automatic reconnecting
    client.loop_forever()    