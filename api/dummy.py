from google.appengine.ext import ndb
from flask import request, jsonify
from flask.views import MethodView
from models.event import Event
from models.show import Show
from models.category import Category
from models.client import Client
from models.price import Price
from models.screen_layout import Screen_Layout
import datetime


class EventView(MethodView):
    def get(self):
        event = Event()
        event.name = '11'
        event.description = 'adsfasdfasd'
        event.active_shows_id = ''
        event.put()
        return jsonify({"Success"})

    def post(self):
        event = Event()
        event.name = request.form['name']
        event.description = request.form['description']
        event.active_shows_id = request.form['active_shows_id']
        event.put()
        return jsonify({'message': "Success"})


class ShowView(MethodView):
    def get(self):
        pass

    def post(self):
        show = Show()
        show.event_id = ndb.Key('Event', request.form['event_id'])
        show.client_id = ndb.Key('Client', request.form['client_id'])
        show.screen_id = ndb.Key('ScreenLayout', request.form['screen_id'])
        show.show_name = request.form['show_name']
        show.datetime = datetime.datetime.now()
        show.seats = request.form['seats']
        show.put()
        return jsonify({'message': "Success"})


class CategoryView(MethodView):
    def get(self):
        pass

    def post(self):
        category = Category()
        category.category_name = request.form['category_name']
        category.screen_id = ndb.Key('Screen', request.form['screen_id'])
        category.seats = request.form['seats']
        category.put()
        return jsonify({'message': "Success"})


class ClientView(MethodView):
    def get(self):
        pass

    def post(self):
        client = Client()
        client.client_name = request.form['client_name']
        client.client_description = request.form['client_description']
        client.screen_list_id = request.form['screen_list_id']
        client.put()
        return jsonify({'message': "Success"})


class PriceView(MethodView):
    def get(self):
        pass

    def post(self):
        price = Price()
        price.show_id = ndb.Key('Show', request.form['show_id'])
        price.category_id = ndb.Key('Category', request.form['category_id'])
        price.amount = int(request.form['price'])
        price.put()
        return jsonify({'message': "Success"})


class ScreenView(MethodView):
    def get(self):
        pass

    def post(self):
        screen = Screen_Layout()
        screen.screen_name = request.form['screen_name']
        screen.client_id = ndb.Key('Client', request.form['client_id'])
        screen.location = request.form['location']
        screen.max_rows = int(request.form['max_rows'])
        screen.max_columns = int(request.form['max_columns'])
        screen.seats = request.form['seats']
        screen.put()
        return jsonify({'message': "Success"})
