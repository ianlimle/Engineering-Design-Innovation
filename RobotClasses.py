# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:56:45 2019

@author: Ian
"""
import RPi.GPIO as GPIO
from transitions import Machine
import json
import paho.mqtt.client as mqtt
import queue
import serial
from time import sleep
import time
import base64
import subprocess    

msgpayload_dict = {}

broker="10.12.108.241"
port=1883
keepalive=60
sendtray = []
ser = serial.Serial()
ser.port = "/dev/ttyACM1"
ser.baudrate = 9600
ser.timeout = 1            #non-block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2

q = queue.Queue(maxsize=4)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#declare pins for actuator and limit switches as GPIO pins
pulPin = 5
dirPin = 6
limit_pin1 = 27
limit_pin2 = 10

#setup the pulse and direction pins of the actuator as outputs
GPIO.setup(pulPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)

#set the 2 limit pins as GPIO inputs each having a pull down resistor 
#prevents floating inputs which willl reduce efficacy of limit switch 
GPIO.setup(limit_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(limit_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#set the pulsepin to default LOW
GPIO.output(pulPin, False)

#global variables to store callback payloads from mqtt broker 
s = 0
e = 0

class MQTTClient():
    
    def on_subscribe(client, userdata, mid, granted_qos):
        print("Subscribed to topic : " + str(mid) + " with Qos " + str(granted_qos))
        pass

    def on_publish(client, userdata, mid):
        print("Published to topic: " + str(mid) + "\n")
        pass

    def on_connect(client, userdata, flags, rc):
        client.subscribe("vfarm/harvest",0)
        client.subscribe("rack/feedback",0)
        client.subscribe("robotrpi/cmnd/begin", 0)
        print("Connected to MQTT broker with result code: " + str(rc) + "\n")
        pass 
    
    def on_disconnect(client, userdata, rc):
        if rc!=0:
            print("Unexpected disconnection") 
            pass
       
    def on_message(client, userdata, msg):
        print("Received message: on topic " + str(msg.topic) 
        + " " + "with QoS " + str(msg.qos))
        
        if str(msg.topic) == "robotrpi/cmnd/begin":
            global e
            e = str(msg.payload.decode())
            print(e)
        
        if str(msg.topic) == "vfarm/harvest":
            h = msg.payload.decode()
            json_acceptable_string = h.replace("'", "\"")
            d = json.loads(json_acceptable_string) 
            print(d)
            q.put(d)
            
        if str(msg.topic) == "rack/feedback":
            global s
            s = str(msg.payload.decode()) 
            print(s)
            
################################## Define camera functions ############################################            
    def capture_plant(tier):
        if tier == 1:
            subprocess.call("fswebcam -d /dev/video1 -r 3280x2464 --no-banner -S0 /home/pi/Desktop/vfarm/1.jpg",shell=True)         
            print("Captured tray: 1")
            subprocess.call("fswebcam -d /dev/video0 -r 3280x2464 --no-banner -S0 /home/pi/Desktop/vfarm/2.jpg",shell=True) 
            print("Captured tray: 2")
            
        if tier == 2:
            subprocess.call("fswebcam -d /dev/video1 -r 3280x2464 --no-banner -S0 /home/pi/Desktop/vfarm/3.jpg",shell=True) 
            print("Captured tray: 3")
            subprocess.call("fswebcam -d /dev/video0 -r 3280x2464 --no-banner -S0 /home/pi/Desktop/vfarm/4.jpg",shell=True) 
            print("Captured tray: 4")
        
    def capture(tier):
        if tier == 1:
            MQTTClient.capture_plant(tier)
            f=open('/home/pi/Desktop/vfarm/1.jpg', "rb")
            byteArray=base64.b64encode(f.read())
            MQTTClient.client.publish("vfarm/1", byteArray)
            time.sleep(1)
            MQTTClient.capture_plant(tier)
            f=open('/home/pi/Desktop/vfarm/2.jpg', "rb")
            byteArray=base64.b64encode(f.read())
            MQTTClient.client.publish("vfarm/2", byteArray)
            time.sleep(1)
            
        if tier == 2:
            MQTTClient.capture_plant(tier)
            f=open('/home/pi/Desktop/vfarm/3.jpg', "rb")
            byteArray=base64.b64encode(f.read())
            MQTTClient.client.publish("vfarm/3", byteArray)
            time.sleep(1)
            MQTTClient.capture_plant(tier)
            f=open('/home/pi/Desktop/vfarm/4.jpg', "rb")
            byteArray=base64.b64encode(f.read())
            MQTTClient.client.publish("vfarm/4", byteArray)
            time.sleep(1)    
            
########################### Define actuator functions ###################################    
    def up(heightinmeter):
        GPIO.output(dirPin, True)
        stop_time = time.time() + heightinmeter*88
        #turn on LED strip just before actuation
        ser.open()
        sleep(1)
        ser.flushOutput()
        ser.flushInput()
        ser.write(b'%d' %(7))
        ser.close()
        while time.time() < stop_time:
            GPIO.output(pulPin, False)
            sleep(0.001)
            GPIO.output(pulPin, True)
            sleep(0.001)          
        #turn off LED strip after actuation
        ser.open()
        sleep(1)
        ser.flushOutput()
        ser.flushInput()
        ser.write(b'%d' %(0))
        ser.close()
        
    def down(heightinmeter):
        GPIO.output(dirPin, False)
        stop_time = time.time() + heightinmeter*88
        #turn on LED strip just before actuation
        ser.open()
        sleep(1)
        ser.flushOutput()
        ser.flushInput()
        ser.write(b'%d' %(7))
        ser.close()
        while time.time() < stop_time:
            GPIO.output(pulPin, False)
            sleep(0.001)
            GPIO.output(pulPin, True)
            sleep(0.001)
            lower_limit = GPIO.input(10)
            if lower_limit == False:
                break
        #turn off LED strip after actuation
        ser.open()
        sleep(1)
        ser.flushOutput()
        ser.flushInput()
        ser.write(b'%d' %(0))
        ser.close()

        
########################### Define serial communication functions for arduino servo release ######################
    def sendforservorelease():
        ser.open()
        sleep(1)
        ser.flushOutput()
        ser.flushInput()
        ser.write(b'%d' %(5))
        print("byte sent: 5")
        feedback = ser.read(1)
        while feedback != b'%d'%(6):
            sleep(0.4)
            feedback = ser.read(1)
            print("waiting...")
            print(feedback)
        print("receiver servo done")
        ser.close()
        
############################ Define line follower commands for arduino  ##########################################################################        
    def startlinefollower():
        ser.open()
        sleep(1)
        ser.flushOutput()
        ser.flushInput()
        ser.write(b'%d' %(1))
        print("byte sent: 1")
        feedback = ser.read(1)
        while feedback != b'%d'%(2):
            sleep(0.4)
            feedback = ser.read(1)
            print("waiting...")
            print(feedback)
        print("reached rack")
        ser.close()
        
    def endlinefollower():
        ser.open()
        sleep(1)
        ser.flushOutput()
        ser.flushInput()
        ser.write(b'%d' %(3))
        print("byte sent: 3")
        feedback = ser.read(1)
        while feedback != b'%d'%(4):
            sleep(0.4)
            feedback = ser.read(1)
            print("waiting...")
            print(feedback)
        print("reached end")
        ser.close()
    
    client = mqtt.Client("robot_rpi", clean_session= False, userdata=None)
    client.on_publish= on_publish
    client.on_subscribe= on_subscribe
    client.on_message= on_message
    client.on_connect= on_connect
    client.on_disconnect= on_disconnect
    client.username_pw_set("pgharvest", "1234")
    client.reconnect_delay_set(min_delay=1, max_delay=6000)
    client.connect(broker, port, keepalive)
            
################################################################################################################
class RobotHarvest(MQTTClient):
    
    states = ['idling', 'followingline1', 'gototier1campos', 'takingtier1pics', 'gototier2campos', 'takingtier2pics', 
              'shiftingdown', 'releasetier1', 'allocatetocollector1', 'releasereceiver1', 
              'shiftingup', 'releasetier2', 'allocatetocollector2', 'releasereceiver2',
              'actuatordefaultpos', 'followingline2']
    
    def __init__(self, *args, **kwargs):
        super(MQTTClient, self).__init__(*args, **kwargs)
        
        #Initialise the state machine
        self.machine = Machine(model= self, #object on which the library attaches trigger functions
                               states= self.states,
                               initial= 'idling')
        
        #add transitions to state machine 
        self.machine.add_transition(trigger= 'StartButtonPressed',
                                    source= 'idling',
                                    dest= 'followingline1',
                                    after= 'go_to_rack',
                                    )
        
        self.machine.add_transition(trigger= 'ReachedRack',
                                    source= 'followingline1',
                                    dest= 'gototier1campos',
                                    after= 'go_to_tier1_cam_pos',
                                    )
          
        self.machine.add_transition(trigger= 'ReachedTier1CamPos',
                                    source= 'gototier1campos',
                                    dest= 'takingtier1pics',
                                    after= 'take_tier1_pics',
                                    )
        
        self.machine.add_transition(trigger= 'TookTier1Pics',
                                    source= 'takingtier1pics',
                                    dest= 'gototier2campos',
                                    after= 'go_to_tier2_cam_pos',
                                    )
        
        self.machine.add_transition(trigger= 'ReachedTier2',
                                    source= 'gototier2campos',
                                    dest= 'takingtier2pics',
                                    after= 'take_tier2_pics',
                                    )
        
        self.machine.add_transition(trigger= 'TookTier2Pics',
                                    source= 'takingtier2pics',
                                    dest= 'shiftingdown',
                                    after= 'go_back_to_tier1',
                                    )
        
        self.machine.add_transition(trigger= 'ReachedTier1',
                                    source= 'shiftingdown',
                                    dest= 'releasetier1',
                                    after= 'ready_for_tier1_slider_release',
                                    )
        
        self.machine.add_transition(trigger= 'RackConfirmation1',
                                    source= 'releasetier1',
                                    dest= 'allocatetocollector1',
                                    after= 'allocate_to_collector1',
                                    )
        
        self.machine.add_transition(trigger= 'ReadyForReceiverRelease1',
                                    source= 'allocatetocollector1',
                                    dest= 'releasereceiver1',
                                    after= 'release_to_collector1',
                                    )
        
        self.machine.add_transition(trigger= 'IsReleasedToCollector1',
                                    source= 'releasereceiver1',
                                    dest= 'shiftingup',
                                    after= 'go_back_to_tier2',
                                    )
        
        self.machine.add_transition(trigger= 'ReachedTier2',
                                    source= 'shiftingup',
                                    dest= 'releasetier2',
                                    after= 'ready_for_tier2_slider_release',
                                    )
        
        self.machine.add_transition(trigger= 'RackConfirmation2',
                                    source= 'releasetier2',
                                    dest= 'allocatetocollector2',
                                    after= 'allocate_to_collector2',
                                    )
        
        self.machine.add_transition(trigger= 'ReadyForReceiverRelease2',
                                    source= 'allocatetocollector2',
                                    dest= 'releasereceiver2',
                                    after= 'release_to_collector2',
                                    )
        
        self.machine.add_transition(trigger= 'IsReleasedToCollector2',
                                    source= 'releasereceiver2',
                                    dest= 'actuatordefaultpos',
                                    after= 'actuator_shift_down',
                                    )
        
        self.machine.add_transition(trigger= 'DefaultPos',
                                    source= 'actuatordefaultpos',
                                    dest= 'followingline2',
                                    after= 'go_to_end',
                                    )
        
    
    def listen_for_startbutton(self):
        print(e)
        while e != "ON":
            sleep(0.8)
            print("listening...")
        MQTTClient.client.publish("robotrpi/state/begin", "ON")    
        print("starting line following")
        return self.StartButtonPressed()
    
#########################################################################################     
    def go_to_rack(self):
        #call function to calibrate and begin line following
        print("go to rack")
        MQTTClient.startlinefollower()
        return self.ReachedRack()
        
#########################################################################################     
    def go_to_tier1_cam_pos(self):
        MQTTClient.up(0.33)
        return self.ReachedTier1CamPos()
    
#########################################################################################    
    def take_tier1_pics(self):
        while q.empty() == False:
            q.get()
        print("take tier1 pics")
        MQTTClient.capture(1)
        return self.TookTier1Pics()

#########################################################################################     
    def go_to_tier2_cam_pos(self):
        print("go to tier 2")
        #call function to move actuator up to tier2 to take pic
        MQTTClient.up(0.40)
        return self.ReachedTier2()
        
#########################################################################################     
    def take_tier2_pics(self):
        print("take tier2 pics")
        MQTTClient.capture(2)
        return self.TookTier2Pics()

#########################################################################################     
    def go_back_to_tier1(self):
        print("go back to tier1")
        #call function to move actuator down to tier 1
        MQTTClient.down(0.81)
        return self.ReachedTier1()
    
#########################################################################################     
    def ready_for_tier1_slider_release(self):
        print("prepare for tier1 slider release")
        for i in range(1,3):
             while q.empty() == True:
                        print("Still waiting for message "+str(i))
             msgpayload = q.get()
             print(msgpayload)
             for key, value in msgpayload.items():
                 msgpayload_dict.update({key: value})
                  
        print(msgpayload_dict)
        MQTTClient.client.publish("rack/tier1/command", str(msgpayload_dict))
       
        global s
        while s != "Slider released":
            sleep(0.8)
            print("waiting for tier1 rack confirmation...")
        s = 0
        return self.RackConfirmation1()    
    
#########################################################################################    
    def allocate_to_collector1(self):
        print("allocate to collector1")
        #shift actuator to collector 1
        MQTTClient.up(0.23)
        return self.ReadyForReceiverRelease1()
    
#########################################################################################     
    def release_to_collector1(self):
        print("prepare for release to collector1")
        #call sendforservorelease() here
        MQTTClient.sendforservorelease()
        return self.IsReleasedToCollector1()
    
#########################################################################################     
    def go_back_to_tier2(self):
        #call function to move actuator down to tier 2
        print("go back to tier2")
        MQTTClient.up(0.23)
        return self.ReachedTier2()
    
#########################################################################################     
    def ready_for_tier2_slider_release(self):
        msgpayload_dict.clear()
        print("prepare for tier2 slider release")
        for i in range(1,3):
             while q.empty() == True:
                        print("Still waiting for message "+ str(i))
             msgpayload = q.get()
             print(msgpayload)
             for key, value in msgpayload.items():
                 msgpayload_dict.update({key: value})
                  
        print(msgpayload_dict)
        MQTTClient.client.publish("rack/tier2/command", str(msgpayload_dict))
       
        global s
        while s != "Slider released":
            sleep(0.8)
            print("waiting for tier2 rack confirmation...")
        s = 0
        return self.RackConfirmation2()   
    
#########################################################################################     
    def allocate_to_collector2(self):
        print("allocate to collector2")
        #shift actuator to collector 1
        MQTTClient.up(0.17)
        return self.ReadyForReceiverRelease2()

#########################################################################################     
    def release_to_collector2(self):
        print("prepare for release to collector2")
        #call sendforservorelease() here
        MQTTClient.sendforservorelease()
        return self.IsReleasedToCollector2()

#########################################################################################     
    def actuator_shift_down(self):
        print("actuator go to default pos")
        MQTTClient.down(0.9)
        return self.DefaultPos()

#########################################################################################     
    def go_to_end(self):
        #call function to calibrate and begin line following
        print("go to end")
        MQTTClient.endlinefollower()
        return self.ReachedStart()