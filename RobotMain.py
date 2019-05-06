# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 16:09:40 2019

@author: Ian
"""

import Classes
from threading import Thread

rack = Classes.RobotHarvest()
mqtt = Classes.MQTTClient()

threadA = Thread(target = mqtt.client.loop_start())
threadB = Thread(target = rack.listen_to_robotrpi())
    
threadA.run()
threadB.run()

