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
import json


class EventView(MethodView):
    def get(self):
        id = 12345
        # query = Event.query(Event.key==ndb.Key('Event',1))
        # res=query.fetch()
        # client = res[0].client_id.get()
        query = Event.query()
        res = query.fetch()
        for each in res:
            print each.client_id
        return str(0)

    def post(self):
        event = Event()
        # event.key = ndb.Key('Event',int(request.form['id']))
        event.client_id = ndb.Key('Client', int(request.form['client_id']))
        event.name = request.form['name']
        event.description = request.form['description']
        event.duration = int(request.form['duration'])
        res = event.put()
        return jsonify({'id': res.id(), 'message': "Success"})


class ShowView(MethodView):
    def get(self):
        show = ndb.Key('Show', 5348024557502464)
        return str(show.get().seats)

    def post(self):
        show = Show()
        # show.key=ndb.Key('Show', int(request.form['id']))
        show.event_id = ndb.Key('Event', int(request.form['event_id']))
        show.client_id = ndb.Key('Client', int(request.form['client_id']))
        show.screen_id = ndb.Key('Screen_Layout', int(request.form['screen_id']))
        show.name = request.form['name']
        show.datetime = datetime.datetime.now()
        screen = ndb.Key('Screen_Layout', int(request.form['screen_id']))
        seats = screen.get().seats
        print type(seats)
        updated_seats = []
        for each in seats:
            newseat = each
            newseat['status'] = 4
            updated_seats.append(newseat)
        show.seats = updated_seats
        res = show.put()

        # The below paragraph should be deleted later
        offset_id = 21
        prices = []
        print show.screen_id
        categories = Category.query(Category.screen_id == show.screen_id).fetch()
        for category in categories:
            price1 = Price(id=show.key.id() + offset_id, show_id=show.key, category_id=category.key, amount=500)
            offset_id += 1
            prices.append(price1)
        print "###"
        print prices
        for price in prices:
            price.put()

        # The above paragraph should be deleted later

        return jsonify({'id': res.id(), 'message': "Success"})


class CategoryView(MethodView):
    def get(self):
        pass

    def post(self):
        category = Category()
        # category.key=ndb.Key('Category', int(request.form['id']))
        category.name = request.form['name']
        category.screen_id = ndb.Key('Screen_Layout', int(request.form['screen_id']))
        category.seats = request.form['seats']
        res = category.put()
        return jsonify({'id': res.id(), 'message': "Success"})


class ClientView(MethodView):
    def get(self):
        id = 12345
        client = ndb.Key('Client', int(id))
        data = client.get()
        print(data)
        return str(data)

    def post(self):
        client = Client()
        # client.key=ndb.Key('Client', int(request.form['id']))
        client.name = request.form['name']
        client.description = request.form['description']
        client.screen_list_id = []
        res = client.put()
        if res:
            return jsonify({'message': "Success", "id": res.id()})
        else:
            return jsonify({'error': 'error message.'})


class PriceView(MethodView):
    def get(self):
        pass

    def post(self):
        price = Price()
        # price.key=ndb.Key('Price', int(request.form['id']))
        price.show_id = ndb.Key('Show', int(request.form['show_id']))
        price.category_id = ndb.Key('Category', int(request.form['category_id']))
        price.amount = int(request.form['amount'])
        res = price.put()
        return jsonify({'id': res.id(), 'message': "Success"})


class ScreenView(MethodView):
    def get(self):
        screen = Screen_Layout().query()
        return str(screen.fetch())
        pass

    def post(self):
        screen = Screen_Layout()
        # screen.key=ndb.Key('Screen_Layout', int(request.form['id']))
        screen.name = request.form['name']
        screen.client_id = ndb.Key('Client', int(request.form['client_id']))
        screen.location = request.form['location']
        screen.max_rows = int(request.form['max_rows'])
        screen.max_columns = int(request.form['max_columns'])
        seats = []
        max_rows = int(request.form['max_rows'])
        max_columns = int(request.form['max_columns'])
        i = 1
        j = 1
        while (i <= max_rows):
            while (j <= max_columns):
                seats.append({'row': i, 'column': j})
                j = j + 1
            j = 1
            i = i + 1
        screen.seats = seats
        result = screen.put()

        # the below paragraph should be deleted later
        category1 = Category(id=screen.key.id() + 23, seats=screen.seats, screen_id=screen.key,
                             name="something something")
        category1.put()
        # the above paragraph should be deleted later

        if result:
            client = screen.client_id.get()
            print client.screen_list_id.append(result.id())
            client.put()
        return jsonify({'id': result.id(), 'seats':screen.seats, 'message': "Success"})



class ScreenViewManual(MethodView):
    def get(self):
        screen = Screen_Layout().query()
        return str(screen.fetch())
        pass

    def post(self):
        screen = Screen_Layout()
        # screen.key=ndb.Key('Screen_Layout', int(request.form['id']))
        screen.name = request.form['name']
        screen.client_id = ndb.Key('Client', int(request.form['client_id']))
        screen.location = request.form['location']
        screen.max_rows = int(request.form['max_rows'])
        screen.max_columns = int(request.form['max_columns'])
        screen.seats = list(json.loads(request.form['seats'].decode('ascii','ignore')))
        print (screen.seats)[2]['row']
        # max_rows = int(request.form['max_rows'])
        # max_columns = int(request.form['max_columns'])
        # i = 1
        # j = 1
        # while (i <= max_rows):
        #     while (j <= max_columns):
        #         seats.append({'row': i, 'column': j})
        #         j = j + 1
        #     j = 1
        #     i = i + 1
        # screen.seats = seats
        result = screen.put()

        # the below paragraph should be deleted later
        category1 = Category(id=screen.key.id() + 23, seats=screen.seats, screen_id=screen.key,
                             name="something something")
        category1.put()
        # the above paragraph should be deleted later

        if result:
            client = screen.client_id.get()
            client.screen_list_id.append(result.id())
            client.put()
        return jsonify({'id': result.id(), 'seats': screen.seats, 'message': "Success"})




class ShowViewManual(MethodView):
    def get(self):
        show = ndb.Key('Show', 5348024557502464)
        return str(show.get().seats)
        pass

    def post(self):
        show = Show()
        # show.key=ndb.Key('Show', int(request.form['id']))
        show.event_id = ndb.Key('Event', int(request.form['event_id']))
        show.client_id = ndb.Key('Client', int(request.form['client_id']))
        show.screen_id = ndb.Key('Screen_Layout', int(request.form['screen_id']))
        show.name = request.form['name']
        show.datetime = datetime.datetime.now()
        screen = ndb.Key('Screen_Layout', int(request.form['screen_id']))
        seats = screen.get().seats
        
        print type(seats)
        updated_seats = []
        for each in seats:
            newseat = each
            newseat['status'] = 4
            updated_seats.append(newseat)
        show.seats = updated_seats
        res = show.put()

        # The below paragraph should be deleted later
        offset_id = 21
        prices = []
        print show.screen_id
        categories = Category.query(Category.screen_id == show.screen_id).fetch()
        for category in categories:
            price1 = Price(id=show.key.id() + offset_id, show_id=show.key, category_id=category.key, amount=500)
            offset_id += 1
            prices.append(price1)
        print "###"
        print prices
        for price in prices:
            price.put()

        # The above paragraph should be deleted later

        return jsonify({'id': res.id(), 'message': "Success"})

