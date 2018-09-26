from google.appengine.ext import ndb
from flask.views import MethodView
from flask import jsonify, request
from models.user import User
from models.user_type import User_Type
from models.user_detail import User_Detail
from models.show import Show
from werkzeug.security import generate_password_hash, check_password_hash
import datetime, json




class UserRegisterView(MethodView):
    def get(self):
        pass

    def post(self):
        # Queries for initial Checks
        USER_EXIST_QUERY=User.query(User.username==request.form['username'])
        EMAIL_EXIST_QUERY=User.query(User.email==request.form['email'])
        PHONE_EXIST_QUERY=User.query(User.contact==request.form['contact'])
        # Pre checks to check exisitng data.
        pre_check={
                            'USER_EXISTS':USER_EXIST_QUERY.fetch(),
                            'EMAIL_EXISTS':EMAIL_EXIST_QUERY.fetch(), 
                            'PHONE_EXISTS':PHONE_EXIST_QUERY.fetch()
                    }
        print(pre_check['PHONE_EXISTS'])
        # Error messages for certain pre checks.
        error_messages={
                            'USER_EXISTS':'Username exists please use another username.',
                            'EMAIL_EXISTS':'Email exists please use another email.',
                            'PHONE_EXISTS':'Phone exists please use another phone.'
                        }
        
        errors=map(lambda k: error_messages[k], filter(lambda k: pre_check[k], pre_check))

        if errors:
            return jsonify({'status': 400, 'message': errors})
        else:
            print 'No User'
            # Add user credentials and minor info
            user=User()
            user.username=request.form['username']
            user.password=generate_password_hash(request.form['password'])
            user.email=request.form['email']
            user.contact=request.form['contact']
            user.description=request.form['description']
            user.created_date=datetime.date.today()
            user_type=User_Type.query(User_Type.name=='User').fetch()
            user.type_id=user_type[0].key

            # Add a User detail
            user_detail=User_Detail()
            user_detail.first_name=request.form['first_name']
            user_detail.middle_name=request.form['middle_name']
            user_detail.last_name=request.form['last_name']
            user_detail.location=request.form['location']
            print type(request.form['dob'].encode('ascii','ignore'))
            user_detail.dob=datetime.datetime.strptime(request.form['dob'], "%d/%m/%Y").date()
            user_detail_key=user_detail.put()

            # Adding a key in userdetail
            user.detail_id=user_detail_key
            res=user.put()

            if res:
                return jsonify({'id': res.id(), 'message': "Username successfully registered."})
            else:
                return jsonify({'status': 500 , 'message': "Error occured"})



class UserLoginView(MethodView):
    def get(self):
        pass

    def post(self):
        query=User.query(User.username==request.form['username']).fetch()
        if query:
            password_check=check_password_hash(query[0].password, request.form['password'])
            if password_check:
                return jsonify({'id': query[0].username, 'message': "User has been successfully Logged in."})    
            else:
                return jsonify({'id': query[0].username, 'message': "Password does not match."})
        else:
            return jsonify({'status': 400, 'message': "User not found consider registering."})
         



class UserTypeView(MethodView):
    def get(self):
        pass

    def post(self):
        query=User_Type.query(User_Type.name==request.form['name']).fetch()
        print query
        if query:
             return jsonify({'id': query[0].key.id(), 'message': "Error: Usertype Exists."})
        else:
            user_type=User_Type()
            user_type.name=request.form['name']
            user_type.permissions=request.form['permissions']
            res=user_type.put()

            if res:
                return jsonify({'status':200, 'id': res.id(), 'message': "UserType successfully created."})
            else:
                return jsonify({'status': 500 , 'message': "Error occured"})



class UserBuySeat(MethodView):
    def get(self):
        pass

    def post(self):
         # Get a show id and json array of seats from post data and complete book operation
        # Incoming post data format:
        # show_id=123123123
        # seat_no={'seats': ["1-2","1-3"]}
        id=int(request.form['show_id'])
        seat_no=request.form['seat_no'].decode('ascii','ignore')    # JSON DECODE to dict
        seat_no=json.loads(seat_no)
        print(seat_no['seats'][0])
        show=Show.get_by_id(id)
        for each in seat_no['seats']:   # For each item in seats check if seats exist and is available for booking.
            if show.seats.get(each):
                if show.seats[each]['status']==4:
                    show.seats[each]['status']=1
                    status=200
                else:
                    return jsonify({'status':404, 'message': "Seat no. "+each+" is unavailable for buying."})
            else:
                return jsonify({'status':404, 'message': "Seat no. "+each+" not found."})
        res=show.put()
        print(res.get().seats)
        return jsonify({'status':200, 'message': "Seat successfully bought."})




class UserBookSeat(MethodView):
    def get(self):
        pass

    def post(self): 
        # Get a show id and json array of seats from post data and complete book operation
        # Incoming post data format:
        # show_id=123123123
        # seat_no={'seats': ["1-2","1-3"]}
        id=int(request.form['show_id'])
        seat_no=request.form['seat_no'].decode('ascii','ignore')    # JSON DECODE to dict
        seat_no=json.loads(seat_no)
        print(seat_no['seats'][0])
        show=Show.get_by_id(id)
        for each in seat_no['seats']:   # For each item in seats check if seats exist and is available for booking.
            if show.seats.get(each):
                if show.seats[each]['status']==4:
                    show.seats[each]['status']=0
                    status=200
                else:
                    return jsonify({'status':404, 'message': "Seat no. "+each+" is unavailable for booking."})
            else:
                return jsonify({'status':404, 'message': "Seat no. "+each+" not found."})
        res=show.put()
        print(res.get().seats)
        return jsonify({'status':200, 'message': "Seat successfully booked."})








