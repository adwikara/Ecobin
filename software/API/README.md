the API provides these mechanisms: 
## 1. GET:
#### /lastObject : 

Pi: get the "type" field to move motors
iOS: display the type and object and percentage on UI
#### /history : 
iOS: to compute stats and display graphs

#### /summary:
iOS: to show summary information from Atlas Database
## 2. PUT
#### /lastObject : 
Pi: to update ONLY the "img" field
BackEnd: update the "type", "object" and "accuracy" fields

Every time backend puts something in lastobject, dump "lastObject" into the database

