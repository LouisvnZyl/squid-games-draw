import json
import numpy as np
import os
import glob
import cv2
import tensorflow as tf
from keras._tf_keras.keras import layers, models
from keras._tf_keras.keras.models import save_model

def draw_image_from_drawing(drawing, img_size=256):
    """
    Converts a drawing (a list of strokes, each a list of points) into an image.
    """
    # Create a blank white canvas
    img = np.ones((img_size, img_size), dtype=np.uint8) * 255  # White background

    # Draw each stroke
    for stroke in drawing:
        # Convert the list of points to an array of coordinates
        points = np.array(stroke, dtype=np.int32)
        
        # For a single stroke, make a polyline to draw it on the image
        if points.shape[0] > 1:
            points = points.reshape((-1, 1, 2))
            cv2.polylines(img, [points], isClosed=False, color=0, thickness=2)  # Black line for stroke
    
    return img

def load_data(root, vfold_ratio=0.2, max_items_per_class=5000, img_size=256):
    # Initialize variables
    images = []
    labels = []
    class_names = []

    # Get all NDJSON files from the root directory (assuming NDJSON file(s) containing data)
    print('Loading Data')
    all_files = glob.glob(os.path.join(root, '*.ndjson'))

    # Load a subset of the data from each file
    print('Processing Data')
    for file_idx, file in enumerate(all_files):
        with open(file, 'r') as f:
            # Read each line in the NDJSON file
            data = [json.loads(line) for line in f]

        # Limit the number of items per class and add to the list
        class_name, _ = os.path.splitext(os.path.basename(file))
        class_names.append(class_name)
        
        class_data = [d for d in data if d['word'] == class_name]  # Filter items by class

        # If we have more than the max items for this class, truncate it
        class_data = class_data[:max_items_per_class]

        # Append the images and labels
        for item in class_data:
            drawing = item['drawing']
            label = item['word']
            
            # Convert drawing to an image
            image = draw_image_from_drawing(drawing, img_size)
            images.append(image)
            labels.append(label)

    # Convert lists to numpy arrays
    images = np.array(images)
    labels = np.array(labels)

    # Label encoding (from string to integer)
    from sklearn.preprocessing import LabelEncoder
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    # Shuffle the dataset
    permutation = np.random.permutation(len(images))
    images = images[permutation]
    labels_encoded = labels_encoded[permutation]

    # Split the data into training and test sets based on the validation fold ratio
    vfold_size = int(len(images) * vfold_ratio)
    x_test = images[:vfold_size]
    y_test = labels_encoded[:vfold_size]

    x_train = images[vfold_size:]
    y_train = labels_encoded[vfold_size:]
    
    x_train = np.expand_dims(x_train, axis=-1) 
    x_test = np.expand_dims(x_test, axis=-1)
    
    print('Data processing done')

    return x_train, y_train, x_test, y_test, class_names

def create_cnn_model(input_shape, num_classes):
    model = models.Sequential()

    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling2D((2, 2)))
    
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(64, (3, 3), activation='relu'))

    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(num_classes, activation='softmax'))
    
    return model

# Example usage
root = 'C:\\Users\\louis\\Downloads\\SGTrain'

x_train, y_train, x_test, y_test, class_names = load_data(root, vfold_ratio=0.2, max_items_per_class=5000)

print(f"Class names: {class_names}")

num_classes = len(class_names)

input_shape = x_train.shape[1:]

model = create_cnn_model(input_shape, num_classes)

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


print('Training Model')
model.fit(x_train, y_train, epochs=5, batch_size=256, validation_data=(x_test, y_test))

test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test accuracy: {test_acc:.4f}")

model.save('Models/cnn_model.h5')