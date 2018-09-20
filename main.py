from flask import Flask, render_template, request
from api.urls import app_add_urls
import datetime

app = Flask(__name__)
app = app_add_urls(app)


@app.route('/')
def index():
    print datetime.datetime.today()
    return render_template('index.html')
