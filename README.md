# 30.007 Engineering Design Innovation
A robotic harvesting platform that automates detection and retrieval of matured crops in multi-tiered, vertical urban farms

## Sensing Rig 
Maturity detection is done using a Mask RCNN pretrained on COCO weights where the class identified is the local lettuce. When ready to harvest, the actuation rig will harvest accordingly.

### Neural Network

#### RPI on Robot
##### Publish topics to server:
For raw image data: 
vfarm/tier01/rack01
vfarm/tier01/rack02
vfarm/tier02/rack01
vfarm/tier02/rack02
##### Publish topics to rack servo:
11/n
12 21 22
##### Subscribe topics from server for harvest commands:
vfarm/harvest
##### Subscribe topics from rack servo as confirmation of open racks:
111 121 211 221

#### Rack Servo
##### Subscribe topics from RPI Robot:
11 12 21 22
##### Publish topics to RPI Robot when gate open:
111 121 211 221

### CSV File Output 
Realtime logging of date, time, exact rack and column of the harvest is done with machine validation vs user validation done to better reinforce learning


## Actuation rig
