import os
import cv2
from random import shuffle, seed
#import unet_config as ucu
from tqdm import tqdm
import numpy as np


# To create a directories from path is not already created
def create_directory(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

# Mapping original image path and ground truth(segmented image) path
def map_img_seg(org_img_dir, seg_img_dir, shuffle=True):
    org_img_paths = os.listdir(org_img_dir)
    org_img_paths.sort()

    seg_img_paths = os.listdir(seg_img_dir)
    seg_img_paths.sort()

    zip_mapped = zip(org_img_paths, seg_img_paths)
    list_mapped = list(zip_mapped)
    if shuffle:
        seed(1)
        shuffle(list_mapped)
    
    return list_mapped


# Read and resize original image
def get_imageArr(path, width, height):
    img = cv2.imread(path, 1)
    img = cv2.resize(img, (width, height))
    return img

# Read and resize seg image
def get_segmentationArr(path, nClasses, width, height):
    img = cv2.imread(path, 1)
    img = cv2.resize(img, (width, height))
    img = img[: , : , 0]
    return img

# Array of all images 
#  
def all_image_array(org_img_dir, seg_img_dir, list_mapped, width, height, NUM_CLASSES):
    X = []
    Y = []

    for i in tqdm(range(len(list_mapped))):
        
        X.append(get_imageArr(os.path.join(org_img_dir, list_mapped[i][0]), width, height))
        Y.append(get_segmentationArr(os.path.join(seg_img_dir, list_mapped[i][1]), NUM_CLASSES, width, height))

    return np.array(X), np.array(Y)


# Sperate part of train image as calib image and store the image in directory
def store_train_cal_img(X_train, Y_train, t_img_dir, t_seg_dir, c_img_dir, c_seg_dir):
    trn_count = int(0)
    cal_cnt = int(0)

    for i in tqdm(range(len(X_train))):
        img = X_train[i]
        seg = Y_train[i]
        
        cv2.imwrite(t_img_dir + '/training_' + str(trn_count) + '.png', img)
        cv2.imwrite(t_seg_dir + '/seg_trn_'+ str(trn_count) + '.png', seg)
        
        if ((trn_count%int(3)) == int(0)):
            cv2.imwrite(c_img_dir +  '/training_'+ str(trn_count) + '.png', img)
            cv2.imwrite(c_seg_dir + '/seg_trn_'+ str(trn_count) + '.png', seg)
            cal_cnt += 1
            
        trn_count += 1

def store_img(X, Y, img_dir, seg_dir):
    count = int(0)
    for i in tqdm(range(len(X))):
        img = X[i]
        seg = Y[i]
        
        cv2.imwrite(img_dir + '/valid_' + str(count) + '.png', img)
        cv2.imwrite(seg_dir + '/seg_v_'+ str(count) + '.png', seg)
        
        count += 1


# Prepare training data 

def normalize_image_arr( path, width, height, norm_factor ):
    img1 = cv2.imread(path, 1)
    img = cv2.resize(img1, (width, height))
    img = img.astype(np.float32)
    img = img/norm_factor - 1.0
    return img

def load_segmentation_arr( path , nClasses, width, height ):
    seg_labels = np.zeros((  width, height  , nClasses ))
    img1 = cv2.imread(path, 1)
    img = cv2.resize(img1, (width, height))
    img = img[:, : , 0]
    for c in range(nClasses):
        seg_labels[: , : , c ] = (img == c ).astype(int)
    return seg_labels

def final_data_prep(org_img_dir, seg_img_dir, width, height, n_classes, norm_factor):
    mapped = map_img_seg(org_img_dir, seg_img_dir, shuffle=False)

    X = []
    Y = []

    for im , seg in tqdm(mapped) :
        X.append( normalize_image_arr(os.path.join(org_img_dir,im), width, height, norm_factor ))
        Y.append( load_segmentation_arr( os.path.join(seg_img_dir,seg) , n_classes , width, height)  )

    return np.array(X), np.array(Y)


if __name__ == "__main__":
    #map_img_seg(ucu.TRAIN_IMG_DIR_INP, ucu.TRAIN_SEG_IMG_DIR_INP)
    pass