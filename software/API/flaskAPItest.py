from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

users = [
    {
        "name": "Orange",
        "accuracy": 80,
        "type": "trash"
    },
    {
        "name": "Bottle",
        "accuracy": 85,
        "type": "recylable"
    },
    {
        "name": "Glass",
        "accuracy": 90 ,
        "type": "recylable"
    }
]

class User(Resource):
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("accuracy")
        parser.add_argument("type")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "accuracy": args["accuracy"],
            "type": args["type"]
        }
        users.append(user)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("accuracy")
        parser.add_argument("type")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["accuracy"] = args["accuracy"]
                user["type"] = args["type"]
                return user, 200

        user = {
            "name": name,
            "accuracy": args["accuracy"],
            "type": args["type"]
        }
        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200

api.add_resource(User, "/user/<string:name>")

app.run(debug=True)
