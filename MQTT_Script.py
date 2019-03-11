# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 20:20:50 2019

@author: Ian
"""
import paho.mqtt.client as paho
import time
import os
import cv2
import imutils
import glob
import csv
import base64

#subclassing the Config class to derive configuration for training
from mrcnn.config import Config

#contains the mask-rcnn model itself
from mrcnn import model as modellib

#visualize output predictions of the mask-rcnn
from mrcnn import visualize

#various utilities leveraged
from imutils import paths 
import random
import argparse

broker = "10.12.218.81"
port = 1883

#keepalive: maximum period in seconds allowed between communications with the broker. 
#If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker
keepalive = 60

DATASET_PATH = os.path.abspath("lettuce")
IMAGES_PATH = os.path.sep.join([DATASET_PATH, "images"])
ANNOT_PATH = os.path.sep.join([DATASET_PATH, "via_region_data.json"])

# initialize the amount of data to use for training
TRAINING_SPLIT = 0.75

# grab all image paths, then randomly select indexes for both training and validation
IMAGE_PATHS = sorted(list(paths.list_images(IMAGES_PATH)))
idxs = list(range(0, len(IMAGE_PATHS)))
random.seed(42)
random.shuffle(idxs)
i = int(len(idxs) * TRAINING_SPLIT)
trainIdxs = idxs[:i]
valIdxs = idxs[i:]

# initialize the class names dictionary
CLASS_NAMES = {1: "Lettuce"}

# initialize the path to the Mask R-CNN pre-trained on COCO
COCO_PATH = "mask_rcnn_coco.h5"

# initialize the name of the directory where logs and output model
# snapshots will be stored
LOGS_AND_MODEL_DIR = os.path.sep.join([DATASET_PATH, "logs_lettuce"])

class LettuceConfig(Config):
	# give the configuration a recognizable name
	NAME = "Lettuce"

	# set the number of GPUs to use training along with the number of
	# images per GPU (which may have to be tuned depending on how
	# much memory your GPU has)
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1

	# set the number of steps per training epoch
	STEPS_PER_EPOCH = len(trainIdxs) // (IMAGES_PER_GPU * GPU_COUNT)

	# number of classes (+1 for the background)
	NUM_CLASSES = len(CLASS_NAMES) + 1

class LettuceInferenceConfig(LettuceConfig):
	# set the number of GPUs and images per GPU (which may be
	# different values than the ones used for training)
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1

	# set the minimum detection confidence (used to prune out false
	# positive detections)
	DETECTION_MIN_CONFIDENCE = 0.9

#initialize the dictionaries for rack_status and switch_status which will serve
#to log the validation status from the machine detection vs user detection (control)
#the data points in the harvest_log csv file will be used for reinforcement learning     
rack_status = {"tier01_rack01": "",
               "tier01_rack02": "",
               "tier02_rack01": "",
               "tier02_rack02": ""
               }

switch_status = {"switch_tier01_rack01": "",
                 "switch_tier01_rack02": "",
                 "switch_tier02_rack01": "",
                 "switch_tier02_rack02": ""
                 }

""" ################################### DEFINE FUNCTIONS AND CALLBACKS BELOW ###########################################
"""
          
#the callback for when the broker has acknowledged the subscription
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic : " + str(mid) + " with Qos " + str(granted_qos) + "/n")
    pass
        
#the callback for when a message has been sent to the broker
def on_publish(client, userdata, mid):
    print("Published to topic: " + str(mid) + "\n")
    pass
    
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc) + "\n")
    """
    the callback for when the client receives a CONNACK response from the server
    the value of rc indicates success or not:
        0: Connection successful    
        1: Connection refused - incorrect protocol version 
        2: Connection refused - invalid client identifier 
        3: Connection refused - server unavailable 
        4: Connection refused - bad username or password 
        5: Connection refused - not authorised 
        6-255: Currently unused
    """
    pass 

#the callback when the client receives a response to disconnect from the server 
def on_disconnect(client, userdata, rc):
    if rc!=0:
        print("Unexpected disconnection") 
    pass

def process_raw_images():
    """
    process image by neural network on remote server
    """
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-w", "--weights",help="optional path to pretrained weights")
    args = vars(ap.parse_args())
    
    # initialize the inference configuration
    config = LettuceInferenceConfig()

	# initialize the Mask R-CNN model for inference
    model = modellib.MaskRCNN(mode="inference", config=config, 
                              model_dir=LOGS_AND_MODEL_DIR)

	# load our trained Mask R-CNN
    weights = args["weights"] if args["weights"] \
        else model.find_last()
    model.load_weights(weights, by_name=True)
    
    class_names = ["BG", "Lettuce"]
    
    colors = visualize.random_colors(len(class_names))

    raw_folderpath = 'vfarm' 
    
    processed_folderpath = 'vfarm_processed'
    
    with open('harvest_log.csv', mode= 'a') as csv_file:
        fieldnames = ['Date', 'Time', 'Row&Column', 'Machine Validation']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
                
        for infile in glob.glob(os.path.join(raw_folderpath, '*.*')):
        
            if infile.split(".")[-1].lower() in {"jpg"}:
                # load the input image
                img = cv2.imread(str(infile))
                #convert it from BGR to RGB channel ordering
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                #resize the image
                img = imutils.resize(img, width=1024)

            	# perform a forward pass of the network to obtain the results
                r = model.detect([img], verbose=1)[0]
                
                # loop over of the detected object's bounding boxes and
                # masks, drawing each as we go along
                for i in range(0, r["rois"].shape[0]):
                    mask = r["masks"][:, :, i]
                    img = visualize.apply_mask(img, mask,(1.0, 0.0, 0.0), alpha=0.5)
                    img = visualize.draw_box(img, r["rois"][i],(1.0, 0.0, 0.0))

            	# convert the image back to BGR so we can use OpenCV's drawing function
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                
                output = visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'], 
                                                     class_names, r['scores'], colors=colors)
                
                # resize the image so it more easily fits on our screen
                output = imutils.resize(output, width=512)
                
                #save the processed image to the vfarm folder
                cv2.imwrite(str(processed_folderpath)+"/"+str(infile), output)
            
                #if there are bounding boxes detected
                if len(r["rois"].shape[0]) > 0:
                    rack_status.update({str(infile): "Y"})
                else:
                    rack_status.update({str(infile): "N"})
                
                writer.writerow({'Date': str(time.strftime("%H:%M:%S")),
                                 'Time': str(time.strftime("%d/%m/%Y")),
                                 'Row&Column': str(infile),
                                 'Machine Validation': str(rack_status[str(infile)])})

    print(rack_status)
    
                
#the callback for when a PUBLISH message is received from the server
#if payload received matches, execute another command/script
def on_message(client, userdata, msg):
    print("Received message: on topic " + str(msg.topic) 
    + " " + "with QoS " + str(msg.qos))

    #if not os.path.exists(str(msg.topic)):
    #    os.mkdir(str(msg.topic))
        
    """
    save image on local machine under folder vfarm
    """ 
    fh = open(str(msg.topic)+".jpg", "wb") 
    fh.write(base64.b64decode(msg.payload))
    fh.close()    
                   
    print("Image decoded and stored in filepath: "+str(msg.topic))
    
    ###############################################################
    
    """
    run the NN and process and save the image
    """        
    process_raw_images()
    
    ###############################################################        
    
    """
    publish motor commands
    """
    #motor_dict = {"tier01_rack01": "turn left, right, up, down",
    #              "tier01_rack02": "turn up, left, right, down",
    #              "tier02_rack01": "turn left, down right, up",
    #              "tier02_rack02": "turn down, left, right, up"}

    
    
    ################################# CLIENT PUBLISHES MOTOR COMMANDS PAYLOAD TO ITS OWN UNQIUE TOPIC ON HOMEASSISTANT #############
    #PUBLISH to topic: vfarm/motors to push motor commands  
    #on the configuration.yaml file, the corresponding topic is under state_topic
    
    #for rack, status in rack_status.items():
    #    if str(status) == "Y":
    #        client.publish("vfarm/motors", str(motor_dict[str(rack)]), qos=0, retain=False)
    
    #with open('harvest_log.csv', mode= 'a') as csv_file:
    #    fieldnames = ['User Validation']
    #    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #    writer.writeheader()
                
        #for j in switch_status.keys():
        #    if base64.b64decode(msg.topic).split("/")[-1] == j:
        #        writer.writerow({'User Validation': str(base64.b64decode(msg.payload))})

############################################################################################################################################    
    
if __name__ == "__main__":
    #instantiate an object of the mqtt client
    """
    arguments: 1.client_id: the unique client id string used when connecting to the broker        
           2.clean_session: a boolean that determines the client type. 
           If True, the broker will remove all information about this client when it disconnects. 
           If False, the client is a durable client and subscription information and queued messages will be retained when the client disconnects.        
           3.userdata: user defined data of any type that is passed as the userdata parameter to callbacks 
    """
    client = paho.Client("rpi_pub", clean_session= False, userdata=None) 

    #assign the functions to the respective callbacks 
    client.on_publish= on_publish
    client.on_message= on_message
    client.on_connect= on_connect
    client.on_disconnect= on_disconnect

    #set a username and password for broker authentification
    #called before connect*()
    #client.username_pw_set("waihong", "1234")

    #client.max_inflight_messages.set()

    client.reconnect_delay_set(min_delay=1, max_delay=180)

    #establish connection to the broker
    client.connect(broker, port, keepalive)

    """
    #SUBSCRIBE to topic:....
    #arguments:1.topic
          2.payload: Passing an int or float will result in the payload being converted to a string representing that number
          If you wish to send a true int/float, use struct.pack() to create the payload you require
          3.qos: quality of service level to use
          4.retain: if set to True, the message will be set as the retained message for the topic 
    """

    ################################# CLIENT SUBSCRIBES TO CORRESPONDING TOPICS FOR RAW IMAGE DATA ############################
    #subscribe and listen to the specific MQTT topic
    #allows multiple topic subscriptions in a single subscription command
    #on the configuration.yaml file, the corresponding topic for the switch is under command_topic....... to receive image data
    client.subscribe("vfarm/tier01_rack01", 0)
    client.subscribe("vfarm/tier01_rack02", 0)
    client.subscribe("vfarm/tier02_rack01", 0)
    client.subscribe("vfarm/tier02_rack02", 0)
    
    ################################# CLIENT SUBSCRIBES TO CORRESPONDING TOPIC FOR USER VALIDATION ON HARVEST ############################
    client.subscribe("vfarm/switch_tier01_rack01", 0)
    client.subscribe("vfarm/switch_tier01_rack02", 0)
    client.subscribe("vfarm/switch_tier02_rack01", 0)
    client.subscribe("vfarm/switch_tier02_rack02", 0)
    
    #the blocking call that processes network traffic, dispatches callbacks and handles automatic reconnecting
    client.loop_forever()  