from events import ListEventView
from api.dummy import EventView, ShowView


def app_add_urls(app):
    app.add_url_rule('/events', view_func=ListEventView.as_view('event_list'), methods=['get', 'post'])
    app.add_url_rule('/dummyevent', view_func=EventView.as_view('ADD_VIEW'), methods=['get','post'])
    app.add_url_rule('/dummyshow', view_func=ShowView.as_view('ADD_SHOW'), methods=['get','post'])

    return app
