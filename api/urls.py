from events import HelloView
from api.dummy import add_event_dummy, add_event


def app_add_urls(app):
    app.add_url_rule('/hello', view_func=HelloView.as_view('hello_view'), methods=['get', 'post'])
    app.add_url_rule('/dummy', 'adding event', add_event, methods=['post'])
    return app
