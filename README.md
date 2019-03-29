# 30.007 Engineering Design Innovation
A robotic harvesting platform that automates detection and retrieval of matured crops in multi-tiered, vertical urban farms

## Sensing Rig 
Maturity detection is done using a Mask RCNN pretrained on COCO weights where the class identified is the local lettuce. When ready to harvest, the actuation rig will harvest accordingly.

### Neural Network

#### RPI on Robot
##### Publish topics to server (for raw image data):
vfarm/tier01_tray01, 
vfarm/tier01_tray02, 
vfarm/tier02_tray01,
vfarm/tier02_tray02
##### Publish topics to rack servo:
11, 12, 21, 22
##### Subscribe topics from server (for harvest commands):
vfarm/harvest
##### Subscribe topics from rack servo (confirmation of slider released):
111, 121, 211, 221

#### Rack Servo
##### Subscribe topics from RPI Robot:
11, 12, 21, 22
##### Publish topics to RPI Robot (confirmation of slider release):
111, 121, 211, 221

### CSV File Output 
Realtime logging of date, time, exact rack and column of the harvest is done with machine validation vs user validation done to better reinforce learning

### Passwords
mqtt server : username : pgharvest
              password : 1234
homeassistant(ui) : username  : project green harvest
                    password : 12345
                   
## Actuation rig

## IP Adresses 
backend(hass/mqtt broker) : 10.12.108.241
robot : 10.12.218.81
rack : 10.12.213.188

### backend steps
## run mqtt broker 
1. sudo /etc/init.d/mosquitto start stop

## run hass ui
1. cd homeassistant/
2. source bin/activate
3. hass
--edit 
sudo leafpad /home/pi/.homeassistant/configuration.yaml

## UI Link
10.12.108.241:8123

### Currently running files
## Rack
 - Packages/ 
  1. Classes.py
  2. __init__.py
  3. main.py
  - Arduino
   1. slider_arduino4.ino
## Robot
1. Robotcam.py
2. receiver_arduino2.ino
3. motor_linefollower.ino
4. actuator.ino

## Backend
1. fakebackend.py
2. configuration.yaml
3. groups.yaml
4. backend.py
