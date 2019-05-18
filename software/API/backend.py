import numpy as np
from PIL import Image
from pymongo import MongoClient
import base64
import os
import json
import time
import requests
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.applications import vgg16
from keras.preprocessing import image
import datetime

##header for PUT request
headers = {
    'Content-type': 'application/json',
}
with open('classes.json') as f:
    classes = json.load(f)
classes = list(classes.keys())
model = load_model("ecobin.h5")
graph = tf.get_default_graph() ##So that flask server doesn't create new threads

'''
Using Keras to generate predictions for the object, the input is a files name
'''       
def predict(filename):
    global graph
    with graph.as_default():
        img = image.load_img(filename, target_size=(224, 224))
        numpy_image =  img_to_array(img)
        numpy_image = np.expand_dims(numpy_image,axis=0)
        ## (1/255) is necessary to scale the accuracy and output accurate percentage
        processed_image = vgg16.preprocess_input(numpy_image.copy())*(1./255)
        predictions = model.predict_proba(processed_image, verbose=1)
        pred = np.argmax(predictions, axis=-1)
        confidence = predictions[0][np.argmax(predictions)]
        print(predictions)
        print(classes[pred[0]])
        return [classes[pred[0]],confidence]

'''
Get the latest image from the API and start processing
'''
def get(img):
    # body = requests.get("http://128.31.22.22:8080/ecobinC/api/v1.0/classify/1", auth=('ecobin-x', 'ecobinpass'))
    # img = img[2:-1] body.json()["string"][2:-1]
    new_im = open("out.jpg", "wb")
    new_im.write(base64.b64decode(img))
    new_im.close()
    return predict("out.jpg")

'''
After predicting the object type, time to create a PUT request
'''
def create_entry(img):
    prediction = get(img)
    ##Threshold if lower than this then trash
    Type = ""
    if (prediction[1] >= 0.65):
        Type = determine(prediction[0])
    else:
        Type = "trash"
    result = {
        "accuracy": prediction[1]*100.,
        "name" : str(prediction[0]), 
        "type" : Type,
        "createdAt" : datetime.datetime.now().strftime("%m-%d-%Y")
    }
    response= requests.put("http://128.31.22.22:8080/ecobinC/api/v1.0/classify/1", auth=('ecobin-x', 'ecobinpass'), headers=headers, data=json.dumps(result))
    print(response)
    return result

'''
Determine if an input is trash or reclyclable by matching up with the list items, hard coded right now
'''
def determine(name):
    trash = ['compostable_containers', 'food', 'fruit', 'leafy_greens']
    recyclable = ['bottle', 'carton', 'cup' , 'general_glass',  'general_plastic', 'general_recyclable', 
    'general_trash', 'metal_can', 'utensils']
    if (name in trash):
        return "trash"
    elif (name in recyclable):
        return "recyclable"