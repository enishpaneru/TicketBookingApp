from flask import Flask, render_template, request
from api.urls import app_add_urls
import datetime
from api.middlewares import UserAuthentication


def add_middlewares(app):
    app.wsgi_app = UserAuthentication.LoggerMiddleware(app.wsgi_app)
    return app


app = Flask(__name__)
app = app_add_urls(app)
app = add_middlewares(app)


@app.route('/')
def index():
    print datetime.datetime.today()
    return render_template('index.html')
