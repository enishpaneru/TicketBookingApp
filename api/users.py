from google.appengine.ext import ndb
from flask.views import MethodView
from flask import jsonify, request
from models.user import User
from models.user_type import User_Type
from models.user_detail import User_Detail
from models.show import Show
from models.ticket import Ticket
from models.category import Category
from models.price import Price
from werkzeug.security import generate_password_hash, check_password_hash

import datetime, json

from middlewares.UserAuthentication import create_user_token


class UserRegisterView(MethodView):
    def get(self):
        pass

    def post(self):
        # Queries for initial Checks
        USER_EXIST_QUERY = User.query(User.username == request.json['username'])
        EMAIL_EXIST_QUERY = User.query(User.email == request.json['email'])
        PHONE_EXIST_QUERY = User.query(User.contact == int(request.json['contact']))
        # Pre checks to check exisitng data.
        pre_check = {
            'USER_EXISTS': USER_EXIST_QUERY.fetch(),
            'EMAIL_EXISTS': EMAIL_EXIST_QUERY.fetch(),
            'PHONE_EXISTS': PHONE_EXIST_QUERY.fetch()
        }
        print(pre_check['PHONE_EXISTS'])
        # Error messages for certain pre checks.
        error_messages = {
            'USER_EXISTS': 'Username exists please use another username.',
            'EMAIL_EXISTS': 'Email exists please use another email.',
            'PHONE_EXISTS': 'Phone exists please use another phone.'
        }

        errors = map(lambda k: error_messages[k], filter(lambda k: pre_check[k], pre_check))

        if errors:
            return jsonify({'status': "error", 'message': errors})
        else:
            # Add user credentials and minor info
            user = User()
            user.username = request.json['username']
            user.password = generate_password_hash(request.json['password'])
            user.email = request.json['email']
            user.contact = int(request.json['contact'])
            user.description = request.json['description']
            user.created_date = datetime.datetime.today()
            user_type = User_Type.query(User_Type.name == 'General').fetch()
            user.type_id = user_type[0].key

            # Add a User detail
            user_detail = User_Detail()
            user_detail.first_name = request.json['first_name']
            user_detail.middle_name = request.json['middle_name']
            user_detail.last_name = request.json['last_name']
            user_detail.location = request.json['location']
            user_detail.dob = datetime.datetime.strptime(request.json['dob'], "%d/%m/%Y").date()
            user_detail_key = user_detail.put()

            # Adding a key in userdetail
            user.detail_id = user_detail_key
            res = user.put()

            if res:
                return jsonify({"status":"success",'id': res.id(), 'message': "Username successfully registered."})
            else:
                return jsonify({'status': "error", 'message': "Error occured"})


class UserLoginView(MethodView):
    def get(self):
        pass

    def post(self):
        query = User.query(User.username == request.json['username']).fetch()
        if query:
            password_check = check_password_hash(query[0].password, request.json['password'])
            if password_check:
                user_kind = query[0].type_id.get().name
                return jsonify({'id': query[0].username, 'token': create_user_token(query[0].key.id(), 86400),
                                'message': "User has been successfully Logged in.", "user_kind": user_kind})
            else:
                return jsonify({'id': query[0].username, 'message': "Password does not match."})
        else:
            return jsonify({'status': 400, 'message': "User not found consider registering."})


class UserTypeView(MethodView):
    def get(self):
        pass

    def post(self):
        query = User_Type.query(User_Type.name == request.json['name']).fetch()
        print query
        if query:
            return jsonify({'id': query[0].key.id(), 'message': "Error: Usertype Exists."})
        else:
            user_type = User_Type()
            user_type.name = request.json['name']
            user_type.permissions = request.json['permissions']
            res = user_type.put()

            if res:
                return jsonify({'status': 200, 'id': res.id(), 'message': "UserType successfully created."})
            else:
                return jsonify({'status': 500, 'message': "Error occured"})


class UserBuySeat(MethodView):
    def get(self):
        pass

    def post(self, event_id, show_id):
        id = int(show_id)
        seat_no = request.json['seat_no']  # JSON DECODE to dict

        show = Show.get_by_id(id)
        for each in seat_no:  # For each item in seats check if seats exist and is available for booking.
            if show.seats.get(each):
                if show.seats[each]['status'] == 4:
                    show.seats[each]['status'] = 1
                    status = 200
                else:
                    return jsonify({'status': 404, 'message': "Seat no. " + each + " is unavailable for buying."})
            else:
                return jsonify({'status': 404, 'message': "Seat no. " + each + " not found."})
        res = show.put()

        seat_list = []
        for seat in seat_no:
            row, col = seat.split('-')
            seat_list.append({'row': int(row), 'column': int(col)})
        # ticket.
        # for price
        screen_id = show.screen_id
        categories = Category.query(Category.screen_id == screen_id).fetch()
        total_price = 0
        for category in categories:
            for each_seat in seat_list:
                for seat in category.seats:
                    if seat['row'] == each_seat['row'] and seat['column'] == each_seat['column']:
                        total_price += Price.query(Price.show_id == show.key,
                                                   Price.category_id == category.key).get().amount
                        continue

        ticket = Ticket(seats=seat_list, total_price=total_price, user_id=request.environ['USER_ID'], show_id=show.key,
                        issued_datetime=datetime.datetime.now())
        res = ticket.put()
        return jsonify({'status': 200, "ticket_id": res.id(), "seats": seat_no, 'message': "Seat successfully bought."})


class UserBookSeat(MethodView):
    def get(self):
        pass

    def post(self, event_id, show_id):
        # Get a show id and json array of seats from post data and complete book operation

        id = int(show_id)
        seat_no = request.json['seat_no']
        show = Show.get_by_id(id)
        for each in seat_no:  # For each item in seats check if seats exist and is available for booking.
            if show.seats.get(each):
                if show.seats[each]['status'] == 4:
                    show.seats[each]['status'] = 0
                    status = 200
                else:
                    return jsonify({'status': 404, 'message': "Seat no. " + each + " is unavailable for booking."})
            else:
                return jsonify({'status': 404, 'message': "Seat no. " + each + " not found."})
        res = show.put()
        print(res.get().seats)
        return jsonify({'status': 200, 'message': "Seat successfully booked."})


class UserDetail(MethodView):
    def get(self):
        user_id = request.environ['USER_ID']
        user = user_id.get()
        user_detail = user.detail_id.get()

        user_name = user.username
        email = user.email
        contact = user.contact
        description = user.description

        first_name = user_detail.first_name
        middle_name = user_detail.middle_name
        last_name = user_detail.last_name
        dob = user_detail.dob
        location = user_detail.location

        return jsonify({'user_name': user_name, 'email': email, 'contact': contact, 'description': description,
                        'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                        'dob': dob, 'location': location})
