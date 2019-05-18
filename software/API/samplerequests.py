import requests
import json

#POST REQUEST
headers = {
    'Content-type': 'application/json',
    }

data = '{"name":"BANANA"}' #change this to see if it works

response = requests.post('http://128.31.22.22:8080/ecobinC/api/v1.0/classify', headers=headers, data=data)
print(response)

#PUT REQUEST

str = 'black cherry'
data = {"string": str}

response = requests.put('http://128.31.22.22:8080/ecobinC/api/v1.0/classify/1', headers=headers, data=json.dumps(data))
print(response)


#DELETE REQUEST
#/3 at the end is a sample request to delete the 3rd dummy ID created

response = requests.delete('http://128.31.22.22:8080/ecobinC/api/v1.0/classify/3')


#GET REQUEST : To get contents of string id/1

response = requests.get('https://ecobin-api.herokuapp.com/ecobinC/api/v1.0/classify/1')
print(response)
print(response.content) #this will print the content of the url onto terminal

