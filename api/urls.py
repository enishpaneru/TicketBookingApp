from events import HelloView
from api.dummy import EventView, ShowView, CategoryView, ClientView, PriceView, ScreenView


def app_add_urls(app):
    app.add_url_rule('/hello', view_func=HelloView.as_view('hello_view'), methods=['get', 'post'])
    app.add_url_rule('/dummyevent', view_func=EventView.as_view('ADD_VIEW'), methods=['get','post'])
    app.add_url_rule('/dummyshow', view_func=ShowView.as_view('ADD_SHOW'), methods=['get','post'])
    app.add_url_rule('/postcategory', view_func=CategoryView.as_view('ADD_CATEGORY'), methods=['get','post'])
    app.add_url_rule('/postclient', view_func=ClientView.as_view('ADD_CLIENT'), methods=['get','post'])
    app.add_url_rule('/postprice', view_func=PriceView.as_view('ADD_PRICE'), methods=['get','post'])
    app.add_url_rule('/postscreen', view_func=ScreenView.as_view('ADD_SCREEN'), methods=['get','post'])
    
    return app
