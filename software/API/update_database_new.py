from pymongo import MongoClient
import requests
import json
import numpy as np
from PIL import Image
import base64
import os
import datetime


headers = {
    'Content-type': 'application/json',
}

#Connect to Mongo Atlas account
client = MongoClient("mongodb+srv://ecobin:Ecobin1!@ecobin-wynhl.mongodb.net/test?retryWrites=true", ssl=True)

#Creates a database called "sample"
db = client.sample

#Creates a collection called "test1" to store upto 5 objects ids 1-5
mycol = db["test1"]

'''
parameter passed in from backend.py
make input format the same as  the  one in the API app.py
'''
def insert(entry):

    #Parse the parameter information from the input dictionary

    # idname = entry.get('name')
    # typename = entry.get('type')
    # accuracynum = entry.get('accuracy')

    result = db.test1.insert_one(entry)
    return result

'''
Counts frequency of items that are recyclable 
or trash and keeps count as more items are thrown into Ecobin
'''
def class_count():
    result = db.test1.aggregate([
                {"$group": {"_id": "$type",
                            "total": {"$sum": 1}}}])

    list1 = list(result)
    recyclable = {}
    trash  = {}
    for item in list1:
        if (item.get("_id") == "recyclable"):
            recyclable = item
        else:
            trash = item
    data = {'recyclable' : recyclable.get("total"), 'trash' : trash.get("total")}
    return data


'''
Calculates average accuracy of the items that are identified
'''
def average_accuracy():
    result2 =  db.test1.aggregate([
                                {"$group": {"_id": "$ne",
                                    "accuracyavg": {"$avg": "$accuracy"}}}]) 
    data2 = dict(list(result2)[0])
    return data2

def daily_push():
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    today_data = list(mycol.find({"createdAt": today}))
    recyclable_count = 0
    trash_count = 0
    for doc in today_data:
        if (doc["type"] == "trash"):
            trash_count += 1
        elif (doc["type"] == "recyclable"):
            recyclable_count += 1
    result = {
        "trash_count": trash_count,
        "recyclable_count": recyclable_count
    }
    print(result)
    response = requests.put('http://128.31.22.22:8080/ecobinC/api/v1.0/classify/weekly', headers=headers, data=json.dumps(result),auth=('ecobin-x', 'ecobinpass'))
    print(response)

def update_API():
    result = class_count()
    result.update(average_accuracy())
    response = requests.put('http://128.31.22.22:8080/ecobinC/api/v1.0/classify/1', headers=headers, data=json.dumps(result),auth=('ecobin-x', 'ecobinpass'))
    print(response)
