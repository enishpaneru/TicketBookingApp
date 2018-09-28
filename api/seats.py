from google.appengine.ext import ndb
from flask.views import MethodView
from flask import jsonify, request
from models.show import Show
import datetime


def change_seat_availability():
    id = int(request.form['show_id'])
    seat_no = request.form['seat_no']
    print(type(id))
    show = Show.get_by_id(id)
    seats = show.seats
    print(seats)
    if show.seats.get(seat_no):
        if show.seats[seat_no]['status'] == 4:
            show.seats[seat_no]['status'] = 3
            show.put()
            print(show.seats)
            return jsonify({'status': 200, 'message': "Seat status changed."})
        else:
            return jsonify({'status': 404, 'message': "Seat is unavailable for changing status."})
    else:
        return jsonify({'status': 404, 'message': "Seat not found."})
