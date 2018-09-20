from flask.views import MethodView
from flask import jsonify, request
from models.event import Event


class HelloView(MethodView):
    def get(self):
        return jsonify({'hello': 'world'})

    def post(self):
        return request.data


class ListEventView(MethodView):
    def get(self):
        query = Event.query().get()
        return jsonify(query)
