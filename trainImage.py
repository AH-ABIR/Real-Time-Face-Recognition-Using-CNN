import os
import numpy as np
from PIL import Image
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Importing model from another file
from Model import model

# Function to resize image
def downsample_image(img):
    img = Image.fromarray(img.astype('uint8'), 'L')
    img = img.resize((32,32), Image.LANCZOS)
    return np.array(img)

# Function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        try:
            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        except:
            continue    
        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faceSamples.append(img_numpy)
        ids.append(id)
    return faceSamples, ids

def TrainImage(path, model_path, message, text_to_speech):
    print ("\n [INFO] Training faces now.")
    faces, ids = getImagesAndLabels(path)
    n_faces = len(set(ids))

    # Initialize the model
    final_model = model((32, 32, 1), n_faces)

    # Preprocess the data
    faces = np.array([downsample_image(img) for img in faces])
    ids = np.asarray(ids)
    faces = faces[:,:,:,np.newaxis]

    # Print the shape of the data
    print("Shape of Data: " + str(faces.shape))
    print("Number of unique faces : " + str(n_faces))

    # Convert labels to one-hot encoding
    ids = to_categorical(ids)

    # Normalize the data
    faces = faces.astype('float32')
    faces /= 255.

    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(faces, ids, test_size=0.2, random_state=0)

    # Compile and train the model
    final_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    final_model.fit(x_train, y_train, batch_size=32, epochs=10, validation_data=(x_test, y_test), shuffle=True)

    # Save the trained model
    final_model.save(model_path)

    res = "Image Trained successfully"  # +",".join(str(f) for f in Id)
    message.configure(text=res)
    text_to_speech(res)

