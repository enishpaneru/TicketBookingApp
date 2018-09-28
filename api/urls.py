from events import ListEventView, ListEventShowView, DetailShowView, EventDetailView
from api.dummy import EventView, ShowView, CategoryView, ClientView, PriceView, ScreenView, ScreenViewManual, \
    ShowViewManual
from events import ListEventView, ListEventShowView, DetailShowView, EventAddView
from api.dummy import EventView, ShowView, CategoryView, ClientView, PriceView, ScreenView, ScreenViewManual, \
    ShowViewManual
from users import UserRegisterView, UserTypeView, UserLoginView, UserBuySeat, UserBookSeat
from api.seats import change_seat_availability
from initrun.datafeed import InitDataFeed
from clients import ClientAdditionView, ClientRegisterView, ListClientEvent, ListClientScreens, ListClientScreenCategory
from clients import ClientAdditionView, ClientRegisterView
from shows import ShowAddView, ShowUpdateView, ShowDeleteMethod
from screens import ScreenAddView, ScreenUpdateView, ScreenDeleteMethod


def app_add_urls(app):
    app = add_events_rule(app)
    app = add_dummy_rule(app)
    app = add_initrun_rule(app)
    app = add_user_rules(app)
    app = action_on_client_rules(app)
    app = add_client_rules(app)
    app = add_shows_rule(app)
    app = add_screens_rule(app)
    return app


def add_events_rule(app):
    app.add_url_rule('/events', view_func=ListEventView.as_view('event_list'), methods=['get', 'post'])

    app.add_url_rule('/events/<event_id>', view_func=EventDetailView.as_view('event_detail'),
                     methods=['get', 'post'])
    app.add_url_rule('/events/<event_id>/shows', view_func=ListEventShowView.as_view('show_list'),
                     methods=['get', 'post'])
    app.add_url_rule('/events/<event_id>/shows/<show_id>', view_func=DetailShowView.as_view('show_detail'),
                     methods=['get', 'post'])
    app.add_url_rule('/events/add', view_func=EventAddView.as_view('add_events'),
                     methods=['get', 'post'])
    return app


def add_shows_rule(app):
    app.add_url_rule('/shows/add', view_func=ShowAddView.as_view('Add_SHOW'), methods=['get', 'post'])
    app.add_url_rule('/shows/delete/<id>', 'Show Delete Request', ShowDeleteMethod, methods=['delete'])
    app.add_url_rule('/shows/update', view_func=ShowUpdateView.as_view('Show UPDATE Request'), methods=['post'])
    return app


def add_screens_rule(app):
    app.add_url_rule('/screens/add', view_func=ScreenAddView.as_view('Add_SCREEN'), methods=['post'])
    app.add_url_rule('/screens/update', view_func=ScreenUpdateView.as_view('UPDATE_SCREEN'), methods=['post'])
    app.add_url_rule('/screens/delete/<id>', 'Screen Delete Request', ScreenDeleteMethod, methods=['delete'])
    return app


def add_user_rules(app):
    app.add_url_rule('/register/user', view_func=UserRegisterView.as_view('ADD_USER_VIEW'), methods=['post'])
    app.add_url_rule('/user/login', view_func=UserLoginView.as_view('LOGIN_USER_VIEW'), methods=['post'])
    app.add_url_rule('/user/addtype', view_func=UserTypeView.as_view('ADD_USER_TYPE_VIEW'), methods=['post'])
    app.add_url_rule('/user/buyseat', view_func=UserBuySeat.as_view('ADD_BUY_SEAT_VIEW'), methods=['post'])
    app.add_url_rule('/user/bookseat', view_func=UserBookSeat.as_view('BOOK_SEAT_VIEW'), methods=['post'])
    return app


def add_client_rules(app):
    app.add_url_rule('/register/client', view_func=ClientRegisterView.as_view('CLIENT_REGISTER_VIEW'), methods=['post'])
    app.add_url_rule('/client/listevents', view_func=ListClientEvent.as_view('LIST_CLIENT_EVENT_VIEW'), methods=['get'])
    app.add_url_rule('/client/listscreens', view_func=ListClientScreens.as_view('LIST_CLIENT_SCREEN_VIEW'),
                     methods=['get'])
    app.add_url_rule('/client/listscreens/<screen_id>/categories',
                     view_func=ListClientScreenCategory.as_view('LIST_CLIENT_SCREEN_CATEGORY_VIEW'), methods=['get'])
    return app


def action_on_client_rules(app):
    app.add_url_rule('/admin/addclient', view_func=ClientAdditionView.as_view('ADD_CLIENT_VIEW'), methods=['post'])
    return app


def add_dummy_rule(app):
    app.add_url_rule('/postevent', view_func=EventView.as_view('ADD_VIEW'), methods=['get', 'post'])
    app.add_url_rule('/postshow', view_func=ShowView.as_view('ADD_SHOW'), methods=['get', 'post'])
    app.add_url_rule('/postcategory', view_func=CategoryView.as_view('ADD_CATEGORY'), methods=['get', 'post'])
    app.add_url_rule('/postclient', view_func=ClientView.as_view('ADD_CLIENT'), methods=['get', 'post'])
    app.add_url_rule('/postprice', view_func=PriceView.as_view('ADD_PRICE'), methods=['get', 'post'])
    app.add_url_rule('/postscreen', view_func=ScreenView.as_view('ADD_SCREEN'), methods=['get', 'post'])
    app.add_url_rule('/postscreenman', view_func=ScreenViewManual.as_view('ADD_MAN_SCREEN'), methods=['get', 'post'])
    app.add_url_rule('/postshowman', view_func=ShowViewManual.as_view('ADD_MAN_SHOW'), methods=['get', 'post'])
    app.add_url_rule('/seatstatus', 'Change Seat Status', change_seat_availability, methods=['post'])
    return app


def add_initrun_rule(app):
    app.add_url_rule('/initdatafeed', "initialdatafeed", InitDataFeed)
    return app
