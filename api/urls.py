from events import ListEventView,ListEventShowView
from api.dummy import EventView, ShowView


def app_add_urls(app):
    app = add_events_rule(app)
    app = add_dummy_rule(app)
    return app


def add_events_rule(app):
    app.add_url_rule('/events', view_func=ListEventView.as_view('event_list'), methods=['get', 'post'])
    app.add_url_rule('/events/<event_id>/shows', view_func=ListEventShowView.as_view('show_list'), methods=['get', 'post'])
    return app


def add_dummy_rule(app):
    app.add_url_rule('/dummyevent', view_func=EventView.as_view('ADD_VIEW'), methods=['get', 'post'])
    app.add_url_rule('/dummyshow', view_func=ShowView.as_view('ADD_SHOW'), methods=['get', 'post'])
    return app
