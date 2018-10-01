from flask.views import MethodView
from flask import jsonify, request
from models.ticket import Ticket
from google.appengine.ext import ndb


class ListTicketView(MethodView):
    def get(self):
        user_id = request.environ['USER_ID']
        tickets = Ticket.query(Ticket.user_id == user_id)
        ticket_list = []
        for ticket in tickets:
            show = ticket.show_id.get()
            event_name = show.event_id.get().name
            total_price = ticket.total_price
            seats = ticket.seats
            ticket_list.append({'show_name': event_name, 'total_price': total_price, 'seats': seats})

        return jsonify(ticket_list)


class DetailTicketView(MethodView):
    def get(self,ticket_id):
        ticket = ndb.Key(Ticket, int(ticket_id))
        show = ticket.show_id.get()
        event_name = show.event_id.get().name
        total_price = ticket.total_price
        seats = ticket.seats
        return jsonify({'show_name': event_name, 'total_price': total_price, 'seats': seats})
