from flask import request, jsonify
from flask.views import MethodView
from models.event import Event



def add_event():
        print('######################')
        print (request.form.name)
        print('######################')
        # event=Event()
        # event.name=request.data['name']
        # event.description=request.data['description']
        # event.active_shows_id=request.data['active_shows_id']
        # event.put()
        return "Success"

def add_event_dummy():
        event=Event()
        event.name='11'
        event.description='adsfasdfasd'
        event.active_shows_id=''
        event.put()
        return "Success"

