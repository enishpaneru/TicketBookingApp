from events import HelloView, ListEventView


def app_add_urls(app):
    app.add_url_rule('/hello', view_func=HelloView.as_view('hello_view'), methods=['get', 'post'])
    app.add_url_rule('/events', view_func=ListEventView.as_view('I_want_to_check_this'), methods=['get'])
    return app
