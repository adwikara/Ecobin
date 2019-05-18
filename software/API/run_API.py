from flask import Flask, jsonify, request

#define app using Flask
app = Flask(__name__)

#parameters = [{'name' : 'trash'}, {'class' : 'trash'}, {'percentage' : '-1'}]
parameters = {'pic' : '-1', 'object':'-1',  'class' : 'trash', 'percentage' : '-1'}

#Getting information from the API server
@app.route('/ecobin', methods=['get'])
def get_parameters():
	return jsonify(parameters)

#Updating information in the API server
@app.route('/ecobin/<string:data_name>', methods=['post'])
def change_data(data_name):
	#Get data to put into the server
	data = {data_name:request.json[data_name]}
	#Update the parameters dictionary
	parameters[data_name] = data[data_name]
	#Return the new dictionary
	return jsonify(parameters)

#Delete dictionary key from dictionary
@app.route('/ecobin', methods=['delete'])
def remove():
	'''
	name = 'object'
	name = 'pic'
	name = 'class'
	'''
	name = 'percentage'
	parameters.pop(name, None)
	return jsonify(parameters)

'''
@app.route('/ecobin/<string:name>', methods=['delete'])
def remove(name):
	parameters.pop(name, None)
	return jsonify(parameters)
'''

if __name__ == '__main__':
	#Run app in debug mode
	#Port is set to 1234, a type of security layer
	app.run(debug=True, port=1234)