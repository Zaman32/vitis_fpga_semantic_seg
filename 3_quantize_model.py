import tensorflow as tf
import unet_config as ucq
import unet_utils as uuq
from tensorflow_model_optimization.quantization.keras import vitis_quantize
import os
import cv2
import numpy as np
    
calib_images = os.listdir(ucq.CALIB_IMG_DIR)
calib_images.sort()

# Normalize the calibration images
X_calib = []

for im in calib_images :
    X_calib.append(uuq.normalize_image_arr(os.path.join(ucq.CALIB_IMG_DIR, im), ucq.WIDTH, ucq.HEIGHT, ucq.NORM_FACTOR))
    
X_calib = np.array(X_calib)

# Non quantized 32-bit floating point model path
float_model = tf.keras.models.load_model(os.path.join('Model', 'keras_model.h5'))
quantizer = vitis_quantize.VitisQuantizer(float_model)
quantized_model = quantizer.quantize_model(calib_dataset=X_calib,calib_batch_size=1)
quantized_model.save(os.path.join('quantized_model', 'doc_quantized_model.h5'))

