from events import HelloView
from api.dummy import EventView, ShowView


def app_add_urls(app):
    app.add_url_rule('/hello', view_func=HelloView.as_view('hello_view'), methods=['get', 'post'])
    app.add_url_rule('/dummyevent', view_func=EventView.as_view('ADD_VIEW'), methods=['get','post'])
    app.add_url_rule('/dummyshow', view_func=ShowView.as_view('ADD_SHOW'), methods=['get','post'])
    
    return app
