import requests
import json

headers = {
    'Content-type': 'application/json',
    }
'''
def postdata():
    #POST REQUEST
    headers = {
        'Content-type': 'application/json',
        }
    data = '{"name":"BANANA"}' #change this to see if it works
    response = requests.post('http://128.31.22.22:8080/ecobinC/api/v1.0/classify', headers=headers, data=data)
    print(response)
'''
def getdata():
    #GET REQUEST
    response = requests.get('http://128.31.22.22:8080/ecobinC/api/v1.0/classify/1')
    #print(response) #prints the status of the request
    #print(response.content) #this will print the content of the url onto terminal
    result = response.json()
    print(result['type']) #prints the type
    return result

def putdata(key, str):
    #PUT REQUEST
    #str = 'black cherry'
    data = {key: str}
    response = requests.put('http://128.31.22.22:8080/ecobinC/api/v1.0/classify/1', headers=headers, data=json.dumps(data))
    print(response)

'''
def deletedata():
    # DELETE REQUEST
    response = requests.delete('https://ecobin-api.herokuapp.com/ecobinC/api/v1.0/classify/1')
'''
getdata()
