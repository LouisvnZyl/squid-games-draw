import numpy as np
import tensorflow as tf
import os
from keras._tf_keras.keras.models import load_model


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model_path = os.path.abspath("Keras_Model/keras_model.h5")
model = load_model(model_path, compile=False)

# Load the labels
labels_path = os.path.abspath("Keras_Model/labels.txt")
with open(labels_path, "r") as file:
    class_names = file.readlines()

# Check if the model and labels are loaded successfully
print(f"Model loaded from: {model_path}")
print(f"Class names loaded from: {labels_path}")
print(f"Total classes: {len(class_names)}")

# What needs to happen here now is to make use of tensorflow and pass through the image that was created by the user and saved.
# This can be done by defining the needed function and importing it and using it in the main running file.