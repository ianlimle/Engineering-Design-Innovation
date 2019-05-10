# 30.007 Engineering Design Innovation
Automation and connectivity are facets of the Industry 4.0 digital transformation wave that Singapore is currently riding on. With such a backdrop, we hope to harness these elements in the state of the art design of a harvesting suite that assists in the detection and retrieval of matured crops in multi-tiered, vertical urban farming applications.
The suite consists of 3 key products coordinated via Internet of Things (IoT) protocols with cloud compute support: 
(i) Harvesting Robot
- autonomous line following navigation
- actuating rig for collection and storage of crops 
- AI-enabled maturity detection algorithm
(ii) Smart Rack
- automated gantry system
- crop tray release control
(iii) Backend Monitoring System
- robot control
- crops monitoring
The IoT Hub enables seamless M2M communication with all 3 features above. We have also introduced cloud compute support for our computationally-intensive image processing tasks and data management. 

## Prototype Demonstration
https://drive.google.com/file/d/1LujWQCsxBQwcrA1VPjlDe_eGRbtkrgQI/view?usp=sharing
## Research Paper
https://drive.google.com/file/d/1NqBNRuVo23LaoQi9IoCKfTkO-04ID2F2/view?usp=sharing
## Poster 
https://drive.google.com/file/d/1BBwjKtgxrbAKLz1QMeWBqWVxtac-kL0W/view?usp=sharing

## Sensing Rig 
Maturity detection is done using a Mask RCNN pretrained on COCO weights. Two classes of lettuce crops are output- either 'Adult' or 'Seedling'. When ready to harvest, the actuation rig will harvest accordingly.

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
homeassistant(UI) : username  : project green harvest
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
On Command Line Terminal of backend, run:
1. cd homeassistant/
2. source bin/activate
3. hass 
(to edit UI) sudo leafpad /home/pi/.homeassistant/configuration.yaml

## UI Link
10.12.108.241:8123

### Currently running files
## Rack
Under rackpackage, run RackMain.py
## Robot
Under robotpackage, run RobotMain.py
## Backend
Run backend.py 
