from flask.views import MethodView
from flask import jsonify, request
from models.event import Event
from models.show import Show
from models.client import Client
from models.screen_layout import Screen_Layout
from google.appengine.ext import ndb


class ListEventView(MethodView):
    def get(self):
        query = Event.query()
        events_list = []
        for each in query.fetch():
            event_id = each.key.id()
            name = each.name
            description = each.description
            client = each.client_id.get()
            client_id = client.key.id()
            client_name = client.name
            events_list.append({'event_id': event_id, 'name': name, 'description': description, 'client_id': client_id,
                                'client_name': client_name})
        return jsonify(events_list)


class ListEventShowView(MethodView):
    def get(self, event_id):
        query = Show.query(Show.event_id == ndb.Key(Event, event_id))
        shows_list = []
        for each in query.fetch():
            show_id = each.key.id()
            client = each.client_id.get()
            screen = each.client_id.get()
            if client is not None:
                client_name = each.client_id.get().name
            else:
                client_name = "Unknown"
            if screen is not None:
                screen_name = each.screen_id.get().name
            else:
                screen_name = "Unknown"
            datetime = each.datetime
            shows_list.append(
                {'show_id': show_id, 'client_name': client_name, 'screen_name': screen_name, 'datetime': datetime})

        return jsonify(shows_list)

