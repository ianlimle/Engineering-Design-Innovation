# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 18:43:35 2019

@author: MX-15
"""
import time
import serial
ser = serial.Serial()
import callbacks
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
ser.port = "/dev/ttyACM0"
#ser.port = "/dev/ttyS2"
ser.baudrate = 9600
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2

sendtray = []



def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic : " + str(mid) + " with Qos " + str(granted_qos) + "/n")
    pass

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

def on_disconnect(client, userdata, rc):
    if rc!=0:
        print("Unexpected disconnection") 
    pass

def on_message(client, userdata, msg):
    print("Received message: on topic " + str(msg.topic) 
    + " " + "with QoS " + str(msg.qos))
    msg_payload = msg.payload
    return msg_payload

def listtray(msg_payload):
    for key in msg_payload :
        if dict[key] == 1 :
            sendtray.append(key)
    return sendtray   

def sendData (sendtray, state):
    ser.open()
    for i in sendtray:
        ser.flushOutput()
        ser.flushInput()
        ser.write(b'%d' %i)
        print("message sent"+i)
        feedback = ser.read(1)
        while feedback != i
             sleep(0.4)
             feedback = ser.read(1)
    ser.close()
    inp = 'sendData done'
    return inp

def listenMQTT():
    client.subscribe("tier1",0)
    client.subscribe("tier2",0)
    if msg_payload 
try: 
    ser.open()

except Exception as e:
    print ("error open serial port: " + str(e))
    exit()

if ser.isOpen():

    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()#flush output buffer, aborting current output 
                 #and discard all that is in buffer

        #write data
        time.sleep(1)
    
        for i in range(1,5,1):
          ser.write(b'%d' %i)
          print("write data: %d"%i)
          ser.flushOutput()
          time.sleep(4)
         
        
        
        ser.close()
    
    except Exception as e1:
        print( "error communicating...: " + str(e1))

else:
    print( "cannot open serial port ")
    

    
    