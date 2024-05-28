import numpy as np
from PIL import Image
import tensorflow as tf
from keras import backend as K
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, BatchNormalization, Dense, Activation, Flatten

def model(input_shape, num_classes):
    # Initialize the model
    model = Sequential([
        Conv2D(512, (3, 3), input_shape=input_shape, activation='relu'),
        Conv2D(256, (3, 3)),
        BatchNormalization(),
        Activation("relu"),
        Conv2D(128, (1, 1)),
        Dropout(0.5),
        BatchNormalization(),
        Activation("relu"),
        Conv2D(64, (3, 3)),
        Dropout(0.5),
        Activation("relu"),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(32, (1, 1), activation='relu'),
        Flatten(),
        Dense(32),
        Dense(num_classes, activation='softmax')
    ])

    # Compile the model
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

    # Print model summary
    model.summary()
    return model
