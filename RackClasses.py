# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:15:19 2019

@author: Ian
"""

from transitions import Machine
import json
import paho.mqtt.client as mqtt
import queue
from threading import Thread
import serial
from time import sleep
    
broker="10.12.108.241"
port=1883
keepalive=60
sendtray = []
ser = serial.Serial()
ser.port = "/dev/ttyACM0"
ser.baudrate = 9600
ser.timeout = 1            #non-block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2
q = queue.Queue()

class MQTTClient():
    
    
    def on_subscribe(client, userdata, mid, granted_qos):
        print("Subscribed to topic : " + str(mid) + " with Qos " + str(granted_qos) + "/n")
        pass

    def on_publish(client, userdata, mid):
        print("Published to topic: " + str(mid) + "\n")
        pass

    def on_connect(client, userdata, flags, rc):
        client.subscribe("rack/tier1/command",0)
        client.subscribe("rack/tier2/command",0)
        print("Connected to MQTT broker with result code: " + str(rc) + "\n")
        
    def on_disconnect(client, userdata, rc):
        if rc!=0:
            print("Unexpected disconnection") 
        pass
    
    def on_message(client, userdata, msg):
        print("Received message: on topic " + str(msg.topic) 
        + " " + "with QoS " + str(msg.qos))
        #q.put(msg.payload)
        print(msg.payload)
        
        s = msg.payload.decode()
        json_acceptable_string = s.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        q.put(d)
        print (d)
        print (q.empty())
    
    def listtray(msg_payload):
        for key , value in msg_payload.items() :
            if value == 1 :
                sendtray.append(int(key))
        sendtray.sort()
        print(sendtray)
        return sendtray   
    
    def sendData (sendtray):
        ser.open()
        sleep(1)
        for i in sendtray:
            ser.flushOutput()
            ser.flushInput()
            ser.write(b'%d' %(i))
            print("byte sent: "+str(i))
            #feedback_string = feedback.decode()
            feedback = ser.read(1)
            while feedback != b'%d'%(i+4):
                sleep(0.4)
                feedback = ser.read(1)
                print("waiting...")
                print(feedback)
            
            #feedback_string = feedback.decode()
            #print(feedback_string)
        ser.close()
        sendtray.clear()
        inp = 'sendData done'
        print(inp)
        return inp, sendtray
    
    client = mqtt.Client("rack_rpi", clean_session=True, userdata=None)

    client.on_publish= on_publish
    client.on-subscribe= on_subscribe
    client.on_message= on_message
    client.on_connect= on_connect
    client.on_disconnect= on_disconnect
    client.username_pw_set("pgharvest", "1234")
    client.reconnect_delay_set(min_delay=1, max_delay=180)
    client.connect(broker, port, keepalive)
   
################################################################################################################
class RackHarvest(MQTTClient):
    
    states = ['listening', 'processing', 'confirming']
    
    def __init__(self, *args, **kwargs):
        super(MQTTClient, self).__init__(*args, **kwargs)
        
        #Initialise the state machine
        self.machine = Machine(model= self, #object on which the library attaches trigger functions
                               states= self.states,
                               initial= 'listening')
        
        #add transitions to state machine 
        self.machine.add_transition(trigger= 'isReceivedfromrobot',
                                    source= 'listening',
                                    dest= 'processing',
                                    after= 'sent_to_and_await_from_rackservo',
                                    )
        
        self.machine.add_transition(trigger= 'isReceivedfromrack',
                                    source= 'processing',
                                    dest= 'confirming',
                                    after= 'sent_to_robotrpi',
                                    )
        
        self.machine.add_transition(trigger= 'isSenttorobot',
                                    source= 'confirming',
                                    dest= 'listening',
                                    after= 'listen_to_robotrpi',
                                    )
        
    
    def listen_to_robotrpi(self):
        print("listening...")
        #if msg.payload is not None:
        while True :
            if q.empty() == False :
                print("received")
                break
        return self.isReceivedfromrobot()
    
    def sent_to_and_await_from_rackservo(self):
        #call listtray() here
        #call sendData() here
        msgpayload = q.get()
        MQTTClient.sendData(MQTTClient.listtray(msgpayload))
       
        return self.isReceivedfromrack()
        
    def sent_to_robotrpi(self):
        ##publish to robotrpi to confirm slider release 
        MQTTClient.client.publish("rack/feedback", "Slider released", qos=0, retain=False)
        sendtray = []
        return self.isSenttorobot()
