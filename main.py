import Classes
from threading import Thread

rack = Classes.RackHarvest()
mqtt = Classes.MQTTClient()
threadA = Thread(target = mqtt.client.loop_start())
threadB = Thread(target = rack.listen_to_robotrpi())
    
threadA.run()
threadB.run()