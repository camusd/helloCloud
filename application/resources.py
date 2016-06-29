import json
from flask import request, abort
from flask_restful import Resource, Api, reqparse
from application import app, api, mongo
from bson.objectid import ObjectId

class ReadingList(Resource):
    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('reading', type=str)
        super().__init__(*args, **kwargs)

    def get(self):
        return [x for x in mongo.db.reading.find()]

    def post(self):
        args = self.parser.parse_args()
        if not args['reading']:
            abort(400)

        jo = json.loads(args['reading'])
        reading_id = mongo.db.readings.insert(jo)
        return mongo.db.readings.find_one({"_id": reading_id})

class Reading(Resource):
    def get(self, reading_id):
        return mongo.db.readings.find_one_or_404({"_id": reading_id})

    def delete(self, reading_id):
        mongo.db.readings.find_one_or_404({"_id": reading_id})
        mongo.db.readings.remove({"_id": reading_id})
        return '', 204

class Status(Resource):
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }

api.add_resource(Status, '/status/')
api.add_resource(ReadingList, '/readings/')
api.add_resource(Reading, '/readings/<ObjectId:reading_id>')
