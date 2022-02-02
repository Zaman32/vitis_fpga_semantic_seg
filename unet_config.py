import cv2
import os
import unet_utils as uuc
import numpy as np


# List of directories

DATASET_DIR = os.path.join(os.getcwd(),'dataset1')

# Input directories
TRAIN_IMG_DIR_INP = os.path.join(DATASET_DIR, "images_prepped_train")
TRAIN_SEG_IMG_DIR_INP = os.path.join(DATASET_DIR, "annotations_prepped_train") 
TEST_IMG_DIR_INP = os.path.join(DATASET_DIR, "images_prepped_test")
TEST_SEG_IMG_DIR_INP = os.path.join(DATASET_DIR, "annotations_prepped_test") 

# Output directories
TRAIN_IMG_DIR = os.path.join(DATASET_DIR, "train_img")
TRAIN_SEG_DIR = os.path.join(DATASET_DIR, "train_seg")
TEST_IMG_DIR = os.path.join(DATASET_DIR, "test_img")
TEST_SEG_DIR = os.path.join(DATASET_DIR, "test_seg")
VALID_IMG_DIR = os.path.join(DATASET_DIR, "valid_img")
VALID_SEG_DIR = os.path.join(DATASET_DIR, "valid_seg")
CALIB_IMG_DIR = os.path.join(DATASET_DIR, "calib_img")
CALIB_SEG_DIR = os.path.join(DATASET_DIR, "calib_seg")


# Image dimentions
HEIGHT = 224
WIDTH = 224

# Normalization factor
NORM_FACTOR = 127.5

# Number of classes
NUM_CLASSES = 12

# Name of classes
CLASS_NAMES = ("Sky",
               "Wall",
               "Pole",
               "Road",
               "Sidewalk",
               "Vegetation",
               "Sign",
               "Fence",
               "vehicle",
               "Pedestrian",
               "Bicyclist",
               "miscellanea")

BATCH_SIZE = 4 #(very small, otherwise OOM error)
EPOCHS = 200

# colors for segmented classes
colorB = [128, 232, 70, 156, 153, 153,  30,   0,  35, 152, 180,  60,   0, 142, 70, 100, 100, 230,  32]
colorG = [ 64,  35, 70, 102, 153, 153, 170, 220, 142, 251, 130,  20,   0,   0,  0,  60,  80,   0,  11]
colorR = [128, 244, 70, 102, 190, 153, 250, 220, 107, 152,  70, 220, 255,   0,  0,   0,   0,   0, 119]
CLASS_COLOR = list()
for i in range(0, 19):
    CLASS_COLOR.append([colorR[i], colorG[i], colorB[i]])
COLORS = np.array(CLASS_COLOR, dtype="float32")