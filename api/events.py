from flask.views import MethodView
from flask import jsonify, request
from models.event import Event
from models.show import Show
from models.client import Client
from models.screen_layout import Screen_Layout
from google.appengine.ext import ndb
from models.category import Category
from models.price import Price


class ListEventView(MethodView):
    def get(self):
        query = Event.query()
        events_list = []
        for each in query.fetch():
            try:
                event_id = each.key.id()
                name = each.name
                description = each.description
                client = each.client_id.get()
                client_id = client.key.id()
                client_name = client.name
                events_list.append(
                    {'event_id': event_id, 'name': name, 'description': description, 'client_id': client_id,
                     'client_name': client_name})
            except Exception as e:
                print e

        return jsonify(events_list)


class EventDetailView(MethodView):
    def check_validation(self, event_id):
        try:
            return int(event_id)
        except:
            return None

    def get(self, event_id):
        event_id = ndb.Key(Event, int(event_id))
        event = event_id.get()
        return jsonify(
            {'client_id': event.client_id.id(), 'client_name': event.client_id.get().name, 'name': event.name,
             'duration': event.duration, 'description': event.description})


class ListEventShowView(MethodView):
    def get(self, event_id):
        event_id = int(event_id)
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


class DetailShowView(MethodView):
    def get(self, event_id, show_id):
        print request.headers
        event_id = int(event_id)
        show_id = int(show_id)
        show = ndb.Key(Show, show_id).get()
        show_screen = show.screen_id.get()
        screen_max_row_col = (show_screen.max_rows, show_screen.max_columns)
        seats_price_category = {}
   
        categories = Category.query(Category.screen_id == show.screen_id).fetch()
        for category in categories:
            price = Price.query(Price.show_id == show.key, Price.category_id == category.key).get()
            if price is not None:
                price_amount = price.amount
            else:
                price_amount = 0
            for seat in category.seats:
                seats_price_category[(seat['row'], seat['column'])] = {'price':price_amount, 'category':category.name}
                

        seats_info = {}
        for seat, description in show.seats.iteritems():
            row, column = seat.split('-')
            row = int(row)
            column = int(column)
            # seat_detail = seat
            seats_info[seat] = {
                'price': seats_price_category[(row, column)]['price'], 'status': description['status'], 'category': seats_price_category[(row, column)]['category']}
            # seat_detail['price'] = seats_price[(seat['row'], seat['column'])]
            # seats_info.append(seat_detail)
        print "now here"
        return jsonify({'show_id': show.key.id(), 'screen_max_row_col': screen_max_row_col, 'screen_seats': seats_info})


class EventAddView(MethodView):
    def get(self):
        pass

    def post(self):
        event = Event()
        # event.key = ndb.Key('Event',int(request.form['id']))
        print '###################'
        print request.is_json
        print request.json
        user_id = request.environ['USER_ID']
        event.client_id = user_id.get().detail_id
        event.name = request.json['name']
        event.description = request.json['description']
        event.duration = int(request.json['duration'])
        res = event.put()
        return jsonify({'id': res.id(), 'message': "Success"})
