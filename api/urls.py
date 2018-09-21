from events import ListEventView, ListEventShowView, DetailShowView
from api.dummy import EventView, ShowView, CategoryView, ClientView, PriceView, ScreenView


def app_add_urls(app):
    app = add_events_rule(app)
    app = add_dummy_rule(app)
    return app


def add_events_rule(app):
    app.add_url_rule('/events', view_func=ListEventView.as_view('event_list'), methods=['get', 'post'])
    app.add_url_rule('/events/<event_id>/shows', view_func=ListEventShowView.as_view('show_list'),
                     methods=['get', 'post'])
    app.add_url_rule('/events/<event_id>/shows/<show_id>', view_func=DetailShowView.as_view('show_detail'),
                    methods=['get', 'post'])
    return app


def add_dummy_rule(app):
    app.add_url_rule('/postevent', view_func=EventView.as_view('ADD_VIEW'), methods=['get', 'post'])
    app.add_url_rule('/postshow', view_func=ShowView.as_view('ADD_SHOW'), methods=['get', 'post'])
    app.add_url_rule('/postcategory', view_func=CategoryView.as_view('ADD_CATEGORY'), methods=['get', 'post'])
    app.add_url_rule('/postclient', view_func=ClientView.as_view('ADD_CLIENT'), methods=['get', 'post'])
    app.add_url_rule('/postprice', view_func=PriceView.as_view('ADD_PRICE'), methods=['get', 'post'])
    app.add_url_rule('/postscreen', view_func=ScreenView.as_view('ADD_SCREEN'), methods=['get', 'post'])
    return app
