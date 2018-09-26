from events import ListEventView, ListEventShowView, DetailShowView
from api.dummy import EventView, ShowView, CategoryView, ClientView, PriceView, ScreenView, ScreenViewManual, ShowViewManual
from users import UserRegisterView, UserTypeView, UserLoginView, UserBuySeat, UserBookSeat
from initrun.datafeed import InitDataFeed


def app_add_urls(app):
    app = add_events_rule(app)
    app = add_dummy_rule(app)
    app = add_initrun_rule(app)
    app=add_user_rules(app)
    return app


def add_events_rule(app):
    app.add_url_rule('/events', view_func=ListEventView.as_view('event_list'), methods=['get', 'post'])
    app.add_url_rule('/events/<event_id>/shows', view_func=ListEventShowView.as_view('show_list'),
                     methods=['get', 'post'])
    app.add_url_rule('/events/<event_id>/shows/<show_id>', view_func=DetailShowView.as_view('show_detail'),
                     methods=['get', 'post'])
    return app


def add_user_rules(app):
    app.add_url_rule('/user/register', view_func=UserRegisterView.as_view('ADD_USER_VIEW'), methods=['post'])
    app.add_url_rule('/user/login', view_func=UserLoginView.as_view('LOGIN_USER_VIEW'), methods=['post'])
    app.add_url_rule('/user/addtype', view_func=UserTypeView.as_view('ADD_USER_TYPE_VIEW'), methods=['post'])
    app.add_url_rule('/user/buyseat', view_func=UserBuySeat.as_view('ADD_BUY_SEAT_VIEW'), methods=['post'])
    app.add_url_rule('/user/bookseat', view_func=UserBookSeat.as_view('BOOK_SEAT_VIEW'), methods=['post'])
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
    app.add_url_rule('/seatstatus', view_func=ShowViewManual.as_view('CHANGE_SEAT_STATUS'), methods=['get', 'post'])
    return app


def add_initrun_rule(app):
    app.add_url_rule('/initdatafeed', "initialdatafeed", InitDataFeed)
    return app
