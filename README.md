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


## Actuation rig
