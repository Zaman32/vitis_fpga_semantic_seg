from random import shuffle
import unet_utils as uut
import unet_config as uct
import unet
import os
import warnings

import tensorflow as tf
from datetime import datetime
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import SGD






warnings.filterwarnings("ignore")


# Avoid OOM errors by setting GPU Memory Consumpthion

gpus = tf.config.experimental.list_physical_devices('GPU')

for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

print("##################################################################")
print("######## Prepare Training Image to use in training ###############")
print("##################################################################")

X_train, Y_train = uut.final_data_prep(uct.TRAIN_IMG_DIR, uct.TRAIN_SEG_DIR, 
uct.WIDTH, uct.HEIGHT, uct.NUM_CLASSES, uct.NORM_FACTOR)


print(X_train.shape)
print(Y_train.shape)

print("##################################################################")
print("######## Prepare Validation Image to use in training ###############")
print("##################################################################")

X_valid, Y_valid = uut.final_data_prep(uct.VALID_IMG_DIR, uct.VALID_SEG_DIR, 
uct.WIDTH, uct.HEIGHT, uct.NUM_CLASSES, uct.NORM_FACTOR)


print(X_valid.shape)
print(Y_valid.shape)


# model object
model = unet.UNET(uct.NUM_CLASSES, uct.HEIGHT, uct.WIDTH, n_filters=16*4, dropout=0.1, batchnorm=True, activation=True)

# Object of SGD
sgd = SGD(learning_rate=1E-6, decay= 5**(-1), momentum=0.5, nesterov=False)

# Compile the model
model.compile(
    loss=tf.keras.losses.CategoricalCrossentropy(),
    optimizer= tf.keras.optimizers.Adam(learning_rate=1e-3),
    metrics=['accuracy']
    
)

# Callbacks - save the best model
model_save_path = os.path.join(os.getcwd(), 'keras_model', 'my_best_model_epoch{epoch:02d}_acc{accuracy:.2f}.hdf5')

model_save_callbacks = tf.keras.callbacks.ModelCheckpoint(
    filepath = model_save_path,
    save_best_only=True,
    monitor = 'val_accuracy',
    mode = 'max'
)

print("##################################################################")
print("############################# Training ###########################")
print("##################################################################")

# Track time
s_time = datetime.now()


# Fit model
hist = model.fit(
    x=X_train, 
    y=Y_train, 
    batch_size=uct.BATCH_SIZE, 
    epochs=uct.EPOCHS, 
    verbose=2, 
    validation_data=(X_valid, Y_valid),
    callbacks = [model_save_callbacks]
)

e_time = datetime.now()

print("Training time: ", (e_time - s_time))

# Saving the model
model.save("final_model.h5")

# Visualize training matrics
plt.figure(figsize=(10,8))
plt.plot(hist.history['loss'], label = 'loss')
plt.plot(hist.history['val_loss'], label = 'val_loss')
plt.show()
# plt.savefig()

plt.figure(figsize=(10,8))
plt.plot(hist.history['accuracy'], label = "accuracy")
plt.plot(hist.history['val_accuracy'], label = 'val_accuracy')
plt.legend()
plt.show()
# plt.savefig()