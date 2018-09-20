from flask.views import MethodView
from flask import jsonify, request


class HelloView(MethodView):
    def get(self):
        return jsonify({'hello': 'world'})

    def post(self):
        return request.data
