
from flask import Flask,jsonify
from flask import abort
from flask import make_response
from flask import request
import datetime
from flask_httpauth import HTTPBasicAuth
import update_database_new as update
from backend import create_entry
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

auth = HTTPBasicAuth()
dailyStats = {
    'day-1': {},
    'day-2': {},
    'day-3': {},
    'day-4': {},
    'day-5': {},
    'day-6': {},
    'day-7': {},
}

def push():
    update.daily_push()
    print("JOB DONE")

cron = BackgroundScheduler(blocking=True)
cron.add_job(func=push, trigger="interval", hours=24, start_date=datetime.datetime(2019, 5, 3, 23, 59, 00, 0))
cron.start()


# scheduler.add_job(func=update.daily_push, trigger="interval", seconds=15)
# scheduler.start()

@auth.get_password
def get_password(username):
    if username == 'ecobin-x':
        return 'ecobinpass'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


app = Flask(__name__)

classify = [
    {
        'id': 1,
        'name': 'nameholder',
        'string': 'stringplaceholder',
        'type': 'Trash',
        'accuracy': 80,
        'recyclable': 0,
        'trash': 0,
        'accuracyavg': 0,
        'capacityTrash': 0,
        'capacityRecycle': 0
    }

]

@app.route('/ecobinC/api/v1.0/classify', methods=['GET'])
@auth.login_required
def get_classify():
    return jsonify({'classify': classify})

@app.route('/ecobinC/api/v1.0/classify/<int:sort_id>', methods=['GET'])
@auth.login_required
def get_idtask(sort_id):
    item = [sort for sort in classify if sort['id'] == sort_id]
    if len(item) == 0:
        abort(404)
    return jsonify(item[0])

@app.route('/ecobinC/api/v1.0/classify', methods=['POST'])
@auth.login_required
def create_sort():
    if not request.json or not 'name' in request.json:
        abort(400)
    new = {
        'id': classify[-1]['id'] + 1,
        'name': request.json['name'],
        'string': request.json.get('string'),
        'type': request.json.get('type'),
        'accuracy': request.json.get('accuracy')
    }
    classify.append(new)
    return jsonify({'new': new}), 201

@app.route('/ecobinC/api/v1.0/classify/<int:sort_id>', methods=['PUT'])
@auth.login_required
def update_sort(sort_id):
    sort = [sort for sort in classify if sort['id'] == sort_id]
    if len(sort) == 0:
        abort(404)
    if not request.json:
        abort(400)
    sort[0]['name'] = request.json.get('name', sort[0]['name'])
    sort[0]['string'] = request.json.get('string', sort[0]['string'])
    sort[0]['type'] = request.json.get('type', sort[0]['type'])
    sort[0]['accuracy'] = request.json.get('accuracy', sort[0]['accuracy'])
    sort[0]['recyclable'] = request.json.get('recyclable', sort[0]['recyclable'])
    sort[0]['trash'] = request.json.get('trash', sort[0]['trash'])
    sort[0]['accuracyavg'] = request.json.get('accuracyavg', sort[0]['accuracyavg'])
    sort[0]['capacityTrash'] = request.json.get('capacityTrash', sort[0]['capacityTrash'])
    sort[0]['capacityRecycle'] = request.json.get('capacityRecycle', sort[0]['capacityTrash'])


    return jsonify({'new': sort[0]})

## This put request is for the Raspberry Pi to upload the image
@app.route('/ecobinC/api/v1.0/classify/img', methods=['PUT'])
@auth.login_required
def put_image():
    img = request.json.get("string")[2:-1]
    entry = create_entry(img)
    db_stat = update.insert(entry)
    response = update_sort(1)
    db_update = update.update_API()
    return jsonify({'img': "Done"})

## For iOS app daily update
@app.route('/ecobinC/api/v1.0/classify/weekly', methods=['PUT'])
@auth.login_required
def putStats():
    if not request.json or not 'trash_count' in request.json:
        abort(400)
    result = request.json
    dailyStats["day-7"] = dailyStats["day-6"]
    dailyStats["day-6"] = dailyStats["day-5"]
    dailyStats["day-5"] = dailyStats["day-4"]
    dailyStats["day-4"] = dailyStats["day-3"]
    dailyStats["day-3"] = dailyStats["day-2"]
    dailyStats["day-2"] = dailyStats["day-1"]
    dailyStats["day-1"] = result
    return jsonify({'putStats': "Done"})

@app.route('/ecobinC/api/v1.0/classify/weekly', methods=['GET'])
@auth.login_required
def get_dailysummary():
    return jsonify(dailyStats)

@app.route('/ecobinC/api/v1.0/classify/<int:sort_id>', methods=['DELETE'])
@auth.login_required
def delete_sort(sort_id):
    sort = [sort for sort in classify if sort['id'] == sort_id]
    if len(sort) == 0:
        abort(404)
    classify.remove(sort[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run('0.0.0.0','8080')
