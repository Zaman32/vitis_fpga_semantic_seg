import unet_utils as uu
import unet_config as uc
import os
import pandas as pd
from random import seed, shuffle
from sklearn.model_selection import train_test_split


# Create all directories
uu.create_directory(uc.TRAIN_IMG_DIR)
uu.create_directory(uc.TRAIN_SEG_DIR)
uu.create_directory(uc.TEST_IMG_DIR)
uu.create_directory(uc.TEST_SEG_DIR)
uu.create_directory(uc.VALID_IMG_DIR)
uu.create_directory(uc.VALID_SEG_DIR)
uu.create_directory(uc.CALIB_IMG_DIR)
uu.create_directory(uc.CALIB_SEG_DIR)

# Get list of image names in the train and train seg directory
train_img_seg_list = uu.map_img_seg(uc.TRAIN_IMG_DIR_INP, uc.TRAIN_SEG_IMG_DIR_INP)

# Read image and convert into array 
X, Y = uu.all_image_array(uc.TRAIN_IMG_DIR_INP, uc.TRAIN_SEG_IMG_DIR_INP, train_img_seg_list, uc.WIDTH, uc.HEIGHT, uc.NUM_CLASSES)

# Split X, Y into train and test set
X_train, X_valid, Y_train, Y_valid = train_test_split(X, Y, test_size = 0.15, random_state = 0)

# Store train and calib image

uu.store_train_cal_img(X_train, Y_train, uc.TRAIN_IMG_DIR, uc.TRAIN_SEG_DIR,
uc.CALIB_IMG_DIR, uc.CALIB_SEG_DIR)

# Store validation image
uu.store_img(X_valid, Y_valid, uc.VALID_IMG_DIR, uc.VALID_SEG_DIR)

# Get list of image names in the test and test seg directory
test_img_seg_list = uu.map_img_seg(uc.TEST_IMG_DIR_INP, uc.TEST_SEG_IMG_DIR_INP)

# Read image and convert into array 
X_test, Y_test = uu.all_image_array(uc.TEST_IMG_DIR_INP, uc.TEST_SEG_IMG_DIR_INP, test_img_seg_list, uc.WIDTH, uc.HEIGHT, uc.NUM_CLASSES)

# Store test image
uu.store_img(X_test, Y_test, uc.TEST_IMG_DIR, uc.TEST_SEG_DIR)

