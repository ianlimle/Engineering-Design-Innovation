import RackClasses
from threading import Thread

rack = RackClasses.RackHarvest()
mqtt = RackClasses.MQTTClient()
threadA = Thread(target = mqtt.client.loop_start())
threadB = Thread(target = rack.listen_to_robotrpi())
    
threadA.run()
threadB.run()