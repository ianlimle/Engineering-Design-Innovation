# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 22:45:09 2019

@author: Ian
"""
import serial
from time import sleep
import time

ser = serial.Serial()
ser.port = "/dev/ttyACM0"
ser.baudrate = 9600
ser.timeout = 1            #non-block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

limit_pin1 =10
limit_pin2 =27
pulPin = 5
dirPin = 6

GPIO.setup(pulPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.output(pulPin, False)
GPIO.setup(limit_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(limit_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def up(heightinmeter):
    ser.open()
    sleep(1)
    ser.flushOutput()
    ser.flushInput()
    ser.write(b'%d' %(7))
    print("byte sent: 7")
    ser.close()
    GPIO.output(dirPin, True)
    stop_time = time.time() + heightinmeter*88
    while time.time() < stop_time:
    #while True:
        GPIO.output(pulPin, False)
        sleep(0.001)
        GPIO.output(pulPin, True)
        sleep(0.001)
    ser.open()
    sleep(1)
    ser.flushOutput()
    ser.flushInput()
    ser.write(b'%d' %(0))
    print("byte sent: 7")
    ser.close()
        
def down(heightinmeter):
    GPIO.output(dirPin, False)
    stop_time = time.time() + heightinmeter*88
    while time.time() < stop_time:
        GPIO.output(pulPin, False)
        sleep(0.001)
        GPIO.output(pulPin, True)
        sleep(0.001)
        lower_limit = GPIO.input(10)
        if lower_limit == False:
            break
        
down(0.9)        