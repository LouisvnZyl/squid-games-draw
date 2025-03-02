import numpy as np
import cv2
import tensorflow as tf
from keras._tf_keras.keras.models import load_model, Model

def load_model() -> Model:
    model = load_model('cnn_model.h5')
    
    return model

def process_image(image_path, img_size=256):
    
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    img = cv2.resize(image, (img_size, img_size))
    
    img = img.astype('float32') / 255
    
    img = np.expand_dims(img, axis=-1)
    
    img - np.expand_dims(img, axis=0)
    
    return image

def predict_image(image_path):
    img = process_image(image_path)
    
    class_names = ['Car', ""]
    
    model = load_model()
    
    prediction = model.predict(img)
    
    predicted_class_idx = np.argmax(prediction, axis=-1)[0]
    
    predicted_class_name = class_names[predicted_class_idx]
    
    return predicted_class_name