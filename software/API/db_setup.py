from pymongo import MongoClient


'''
email: adwikara@bu.edu
username: ecobin
password: Ecobin1!
"mongodb://username:password!@ecobin-shard-00-00-wynhl.mongodb.net:27017,ecobin-shard-00-01-wynhl.mongodb.net:27017,ecobin-shard-00-02-wynhl.mongodb.net:27017/test?ssl=true&replicaSet=ecobin-shard-0&authSource=admin&retryWrites=true"
pip install pymongo[snappy,gssapi,srv,tls]
'''

parameters = {'_id':2, 'pic' : '-1', 'object':'-1',  'class' : 'trash', 'percentage' : '100'}

#Connect to Mongo Atlas account
client = MongoClient("mongodb://ecobin:Ecobin1!@ecobin-shard-00-00-wynhl.mongodb.net:27017,ecobin-shard-00-01-wynhl.mongodb.net:27017,ecobin-shard-00-02-wynhl.mongodb.net:27017/test?ssl=true&replicaSet=ecobin-shard-0&authSource=admin&retryWrites=true")

#Creates a database called "sample"
db = client.sample

#Creates a collection called "testing"
mycol = client["test1"]
mycol2 = client["test2"]
mycol3 = client["testing"]

#Inserts information to the collection
result = db.test1.insert_one(parameters)
result = db.test2.insert_one(parameters)
result = db.testing.insert_one(parameters)
