import json
import numpy as np
import tensorflow as tf
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras._tf_keras.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import cv2

def load_data(ndJson_file):
    images = []
    lables = []
    
    with open(ndJson_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            image_path = data['image_path']
            label = data['label']
            
            image = cv2.imread(image_path)
            image = cv2.resize(image, (128, 128))
            image = image.astype('float32') / 255.0
            
            images.append(images)
            lables.append(label)
            
    images = np.array(images)
    lables = np.array(lables)
    
    return images, lables