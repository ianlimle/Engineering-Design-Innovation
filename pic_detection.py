# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 01:22:05 2019

@author: Ian
"""
#USAGE
# python pic_detection.py --mode predict --image examples/.jpg
# python pic_detection.py --mode predict --image examples/.jpg  --weights logs/....


#IMPORT NECESSARY PACKAGES
#########################################################################
#create additional training data by applying random transformations
#reduces overfitting and allows greater generalizability
#from imgaug import augmenters as iaa

#subclassing the Config class to derive configuration for training
from mrcnn.config import Config

#contains the mask-rcnn model itself
from mrcnn import model as modellib

#visualize output predictions of the mask-rcnn
from mrcnn import visualize

#various utilities leveraged
from mrcnn import utils
from imutils import paths
import numpy as np 
import argparse
import imutils
import skimage
import random
import json
import cv2
import os

# initialize the dataset path, images path, and annotations file path
DATASET_PATH = os.path.abspath("lettuce")
IMAGES_PATH = os.path.sep.join([DATASET_PATH, "images"])
ANNOT_PATH = os.path.sep.join([DATASET_PATH, "via_region_data.json"])

# initialize the amount of data to use for training
TRAINING_SPLIT = 0.75

# grab all image paths, then randomly select indexes for both training
# and validation
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
    
if __name__ == "__main__":
	# construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-w", "--weights",help="optional path to pretrained weights")
    ap.add_argument("-i", "--image",help="optional path to input image to segment")
    args = vars(ap.parse_args())
    
	# initialize the inference configuration
    config = LettuceInferenceConfig()

	# initialize the Mask R-CNN model for inference
    model = modellib.MaskRCNN(mode="inference", config=config, model_dir=LOGS_AND_MODEL_DIR)

	# load our trained Mask R-CNN
    weights = args["weights"] if args["weights"] \
        else model.find_last()
    model.load_weights(weights, by_name=True)
    
    class_names = ["BG", "Lettuce"]
    
    colors = visualize.random_colors(len(class_names))

	# load the input image, convert it from BGR to RGB channel
	# ordering, and resize the image
    image = cv2.imread(args["image"])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = imutils.resize(image, width=1024)

	# perform a forward pass of the network to obtain the results
    r = model.detect([image], verbose=1)[0]
    """    
    # loop over of the detected object's bounding boxes and
	# masks, drawing each as we go along
    for i in range(0, r["rois"].shape[0]):
        mask = r["masks"][:, :, i]
        image = visualize.apply_mask(image, mask,(1.0, 0.0, 0.0), alpha=0.5)
        image = visualize.draw_box(image, r["rois"][i],(1.0, 0.0, 0.0))

	# convert the image back to BGR so we can use OpenCV's drawing function
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	# loop over the predicted scores and class labels
    for i in range(0, len(r["scores"])):
		# extract the bounding box information, class ID, label,
        # and predicted probability from the results
        (startY, startX, endY, end) = r["rois"][i]
        classID = r["class_ids"][i]
        label = CLASS_NAMES[classID]
        score = r["scores"][i]

		# draw the class label and score on the image
        text = "{}: {:.4f}".format(label, score)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.putText(image, text, (startX, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
    # resize the image so it more easily fits on our screen
    image = imutils.resize(image, width=512)
    """
    output = visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                                         class_names, r['scores'], colors=colors)

	# show the output image
    #cv2.imshow("Output", image)
    cv2.imshow("Output", output)
    cv2.waitKey(0)