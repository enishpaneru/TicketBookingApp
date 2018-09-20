from google.appengine.ext import ndb
from flask import request, jsonify
from flask.views import MethodView
from models.event import Event
from models.show import Show
import datetime





class EventView(MethodView):
    def get(self):
        event=Event()
        event.name='11'
        event.description='adsfasdfasd'
        event.active_shows_id=''
        event.put()
        return jsonify({"Success"})


    def post(self):
        event=Event()
        event.name=request.form['name']
        event.description=request.form['description']
        event.active_shows_id=request.form['active_shows_id']
        event.put()
        return jsonify({'message':"Success"})



class ShowView(MethodView):
    def get(self):
        pass


    def post(self):
        show=Show()
        show.event_id=ndb.Key('Event',request.form['event_id'])
        show.client_id=ndb.Key('Client',request.form['client_id'])
        show.screen_id=ndb.Key('ScreenLayout',request.form['screen_id'])
        show.show_name=request.form['show_name']
        show.datetime=datetime.datetime.now()
        show.seats=request.form['seats']
        show.put()
        return jsonify({'message':"Success"})


class CategoryView(MethodView):
    def get(self):
        pass


    def post(self):
        show=Show()
        show.event_id=ndb.Key('Event',request.form['event_id'])
        show.client_id=ndb.Key('Client',request.form['client_id'])
        show.screen_id=ndb.Key('ScreenLayout',request.form['screen_id'])
        show.show_name=request.form['show_name']
        show.datetime=request.form['datetime']
        show.seats=request.form['seats']
        show.put()
        return jsonify({'message':"Success"})







