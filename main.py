from flask import Flask, render_template, request,redirect,url_for
from api.urls import app_add_urls
import datetime
from api.middlewares import UserAuthentication
from flask_cors import CORS

def add_middlewares(app):
    app.wsgi_app = UserAuthentication.LoggerMiddleware(app.wsgi_app)
    return app


app = Flask(__name__)
CORS(app)

app = app_add_urls(app)
app = add_middlewares(app)



@app.route('/')
def index():
    return redirect(url_for('event_list'))
