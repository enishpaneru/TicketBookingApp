from events import HelloView


def app_add_urls(app):
    app.add_url_rule('/hello', view_func=HelloView.as_view('hello_view'), methods=['get', 'post'])
    return app
