from google.appengine.ext import ndb
from flask.views import MethodView
from flask import jsonify, request
from models.user import User
from models.user_type import User_Type
from models.client import Client
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class UserRegisterView(MethodView):
    def get(self):
        pass

    def post(self):
        query=User.query(User.username==request.form['username']).fetch()
        if query:
            return jsonify({'id': query[0].username, 'message': "Username Exists please use another username"})
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

