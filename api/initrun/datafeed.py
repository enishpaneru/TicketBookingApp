from datetime import datetime

from google.appengine.ext import ndb

from models.category import Category
from models.client import Client
from models.event import Event
from models.price import Price
from models.screen_layout import Screen_Layout
from models.show import Show


def InitDataFeed():
    create_clients()
    create_events()
    create_screens()
    create_shows()
    create_categories()
    create_prices()
    return 'Success'


def create_clients():
    client1 = Client(id=12345, name="QFX Movies",
                     description="QFX Movies is a good movie hall with different auditoriums.",
                     screen_list_id=[1, 2])
    client2 = Client(id=123456, name="BSR Movies",
                     description="BSR Movies is one of the finest movie hall with dolby sound support.",
                     screen_list_id=[3, 4])

    client1.put()
    client2.put()


def create_events():
    event1 = Event(id=1, client_id=ndb.Key(Client, 12345), name="3 Idiots",
                   description="3 Idiots is a beautiful movie.", duration=180)
    event2 = Event(id=2, client_id=ndb.Key(Client, 12345), name="The Godzilla",
                   description="The godzilla is a dinosaur.", duration=180)
    event3 = Event(id=3, client_id=ndb.Key(Client, 123456), name="Avengers Infinity wars",
                   description="Avenger Infinity wars is a movie by marvel.", duration=180)
    event4 = Event(id=4, client_id=ndb.Key(Client, 123456), name="The Godzilla",
                   description="The godzilla is a dinosaur.", duration=180)
    ndb.put_multi([event1, event2, event3, event4])


def create_screens():
    screen1 = Screen_Layout(id=1, name="A1", client_id=ndb.Key(Client, 12345), location="Sundhara, Kathmandu",
                            max_rows=2, max_columns=2,
                            seats=[{'row': 1, 'column': 1}, {'row': 1, 'column': 2}, {'row': 2, 'column': 1},
                                   {'row': 2, 'column': 2}])
    screen2 = Screen_Layout(id=2, name="B1", client_id=ndb.Key(Client, 12345), location="Sundhara, Kathmandu",
                            max_rows=2, max_columns=2,
                            seats=[{'row': 1, 'column': 1}, {'row': 1, 'column': 2}, {'row': 2, 'column': 1},
                                   {'row': 2, 'column': 2}])
    screen3 = Screen_Layout(id=3, name="AD 1", client_id=ndb.Key(Client, 123456), location="New Buspark, Kathmandu",
                            max_rows=2, max_columns=2,
                            seats=[{'row': 1, 'column': 1}, {'row': 1, 'column': 2}, {'row': 2, 'column': 1},
                                   {'row': 2, 'column': 2}])
    screen4 = Screen_Layout(id=4, name="AD 2", client_id=ndb.Key(Client, 123456), location="New Buspark, Kathmandu",
                            max_rows=2, max_columns=2,
                            seats=[{'row': 1, 'column': 1}, {'row': 1, 'column': 2}, {'row': 2, 'column': 1},
                                   {'row': 2, 'column': 2}])
    ndb.put_multi([screen1, screen2, screen3, screen4])


def create_shows():
    show1 = Show(id=1, event_id=ndb.Key(Event, 1), client_id=ndb.Key(Client, 12345),
                 screen_id=ndb.Key(Screen_Layout, 1),
                 datetime=datetime.strptime("2018-09-24 12:00:00.0", '%Y-%m-%d %H:%M:%S.%f'),
                 seats=[{'row': 1, 'column': 1, 'status': 4}, {'row': 1, 'column': 2, 'status': 4},
                        {'row': 2, 'column': 1, 'status': 4}, {'row': 2, 'column': 2, 'status': 4}])
    show2 = Show(id=2, event_id=ndb.Key(Event, 2), client_id=ndb.Key(Client, 12345),
                 screen_id=ndb.Key(Screen_Layout, 2),
                 datetime=datetime.strptime("2018-09-20 12:00:00.0", '%Y-%m-%d %H:%M:%S.%f'),
                 seats=[{'row': 1, 'column': 1, 'status': 4}, {'row': 1, 'column': 2, 'status': 4},
                        {'row': 2, 'column': 1, 'status': 4}, {'row': 2, 'column': 2, 'status': 4}])
    show3 = Show(id=3, event_id=ndb.Key(Event, 4), client_id=ndb.Key(Client, 123456),
                 screen_id=ndb.Key(Screen_Layout, 3),
                 datetime=datetime.strptime("2018-09-20 12:00:00.0", '%Y-%m-%d %H:%M:%S.%f'),
                 seats=[{'row': 1, 'column': 1, 'status': 4}, {'row': 1, 'column': 2, 'status': 4},
                        {'row': 2, 'column': 1, 'status': 4}, {'row': 2, 'column': 2, 'status': 4}])
    show4 = Show(id=4, event_id=ndb.Key(Event, 3), client_id=ndb.Key(Client, 123456),
                 screen_id=ndb.Key(Screen_Layout, 4),
                 datetime=datetime.strptime("2018-09-20 12:00:00.0", '%Y-%m-%d %H:%M:%S.%f'),
                 seats=[{'row': 1, 'column': 1, 'status': 4}, {'row': 1, 'column': 2, 'status': 4},
                        {'row': 2, 'column': 1, 'status': 4}, {'row': 2, 'column': 2, 'status': 4}])
    ndb.put_multi([show1, show2, show3, show4])


def create_categories():
    category1 = Category(id=1, name="Balcony", screen_id=ndb.Key(Screen_Layout, 1),
                         seats=[{'row': 2, 'column': 1}, {'row': 2, 'column': 2}])
    category2 = Category(id=2, name="Normal", screen_id=ndb.Key(Screen_Layout, 1),
                         seats=[{'row': 1, 'column': 1}, {'row': 1, 'column': 2}])
    category3 = Category(id=3, name="Normal", screen_id=ndb.Key(Screen_Layout, 2),
                         seats=[{'row': 1, 'column': 1}, {'row': 1, 'column': 2}, {'row': 2, 'column': 1},
                                {'row': 2, 'column': 2}])
    category4 = Category(id=4, name="Normal", screen_id=ndb.Key(Screen_Layout, 3),
                         seats=[{'row': 1, 'column': 1}, {'row': 1, 'column': 2}, {'row': 2, 'column': 1},
                                {'row': 2, 'column': 2}])
    category5 = Category(id=5, name="Premium", screen_id=ndb.Key(Screen_Layout, 4),
                         seats=[{'row': 1, 'column': 1}, {'row': 1, 'column': 2}, {'row': 2, 'column': 1},
                                {'row': 2, 'column': 2}])
    ndb.put_multi([category1, category2, category3, category4, category5])


def create_prices():
    price1 = Price(id=1, show_id=ndb.Key(Show, 1), category_id=ndb.Key(Category, 1), amount=500)
    price2 = Price(id=2, show_id=ndb.Key(Show, 1), category_id=ndb.Key(Category, 2), amount=200)
    price3 = Price(id=3, show_id=ndb.Key(Show, 2), category_id=ndb.Key(Category, 3), amount=200)
    price4 = Price(id=4, show_id=ndb.Key(Show, 3), category_id=ndb.Key(Category, 4), amount=200)
    price5 = Price(id=5, show_id=ndb.Key(Show, 4), category_id=ndb.Key(Category, 4), amount=1000)
    ndb.put_multi([price1, price2, price3, price4, price5])
