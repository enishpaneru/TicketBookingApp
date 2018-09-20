from api.dummy import add_event_dummy
from events import ListEventView


def app_add_urls(app):
    app.add_url_rule('/dummy', 'adding event', add_event_dummy)
    app.add_url_rule('/events', view_func=ListEventView.as_view('event_list'), methods=['get', 'post'])
    return app
