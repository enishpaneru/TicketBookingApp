from flask.views import MethodView
from flask import jsonify, request
from models.event import Event


class ListEventView(MethodView):
    def get(self):
        query = Event.query()
        return jsonify(
            [{'event_id': each.key.id(), 'name': each.name, 'description': each.description} for each in query.fetch()])
