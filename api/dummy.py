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
        id=12345
        # query = Event.query(Event.key==ndb.Key('Event',1))
        # res=query.fetch()
        # client = res[0].client_id.get()
        query=Event.query()
        res=query.fetch()
        for each in res:
            print each.client_id
        return str(0)

    def post(self):
        event=Event()
        # event.key = ndb.Key('Event',int(request.form['id']))
        event.client_id=ndb.Key('Client',int(request.form['client_id']))
        event.name=request.form['name']
        event.description=request.form['description']
        event.duration=int(request.form['duration'])
        res=event.put()
        return jsonify({'id': res.id(), 'message': "Success"})


class ShowView(MethodView):
    def get(self):
        pass

    def post(self):
        show = Show()
        # show.key=ndb.Key('Show', int(request.form['id']))
        show.event_id = ndb.Key('Event', int(request.form['event_id']))
        show.client_id = ndb.Key('Client', int(request.form['client_id']))
        show.screen_id = ndb.Key('Screen_Layout', int(request.form['screen_id']))
        show.name = request.form['name']
        show.datetime = datetime.datetime.now()
        show.seats = request.form['seats']
        res=show.put()
        return jsonify({'id':res.id(),'message': "Success"})


class CategoryView(MethodView):
    def get(self):
        pass

    def post(self):
        category = Category()
        # category.key=ndb.Key('Category', int(request.form['id']))
        category.name = request.form['name']
        category.screen_id = ndb.Key('Screen_Layout', int(request.form['screen_id']))
        category.seats = request.form['seats']
        res=category.put()
        return jsonify({'id':res.id(),'message': "Success"})


class ClientView(MethodView):
    def get(self):
        id=12345
        client=ndb.Key('Client', int(id))
        data=client.get()
        print(data)        
        return str(data)
        

    def post(self):
        client = Client()
        # client.key=ndb.Key('Client', int(request.form['id']))
        client.name = request.form['name']
        client.description = request.form['description']
        client.screen_list_id = []
        res=client.put()
        if res:
            return jsonify({'message': "Success", "id": res.id()})
        else:
            return jsonify({'error':'error message.'})




class PriceView(MethodView):
    def get(self):
        pass

    def post(self):
        price = Price()
        # price.key=ndb.Key('Price', int(request.form['id']))
        price.show_id = ndb.Key('Show', int(request.form['show_id']))
        price.category_id = ndb.Key('Category', int(request.form['category_id']))
        price.amount = int(request.form['amount'])
        res=price.put()
        return jsonify({'id':res.id(),'message': "Success"})


class ScreenView(MethodView):
    def get(self):
        pass

    def post(self):
        screen=Screen_Layout()
        # screen.key=ndb.Key('Screen_Layout', int(request.form['id']))
        screen.name=request.form['name']
        screen.client_id=ndb.Key('Client',int(request.form['client_id']))
        screen.location=request.form['location']
        screen.max_rows=int(request.form['max_rows'])
        screen.max_columns=int(request.form['max_columns'])
        screen.seats=request.form['seats']
        result=screen.put()
        if result:
            client=screen.client_id.get()
            print client.screen_list_id.append(result.id())
            client.put()
        return jsonify({'id': result.id(), 'message':"Success"})


    









