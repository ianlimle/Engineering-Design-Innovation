# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 16:09:40 2019

@author: Ian
"""

import RobotClasses
from threading import Thread

robot = RobotClasses.RobotHarvest()
mqtt = RobotClasses.MQTTClient()

threadA = Thread(target = mqtt.client.loop_start())
threadB = Thread(target = robot.listen_for_startbutton())
    
threadA.run()
threadB.run()

