from google.appengine.ext import ndb
from flask.views import MethodView
from flask import jsonify, request
from models.user import User
from models.user_type import User_Type
from models.user_detail import User_Detail
from models.client import Client
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from Mail import MailService
from middlewares.UserAuthentication import create_user_token, check_user_token


class ClientRegisterView(MethodView):
    def get(self):
        pass

    def post(self):
        print "in post"
        query = User.query(User.username == request.form['username']).fetch()
        if query:
            return jsonify({'id': query[0].username, 'message': "Username Exists please use another username"})
        else:

            # check the association and validity of the client create account token
            client_id = self.check_client_token(request.headers)
            if not client_id:
                return jsonify(
                    {'message': "Token validation gone wrong please request a new registration link from the admins"})

            # Add user credentials and minor info
            user = User()
            user.username = request.form['username']
            user.password = generate_password_hash(request.form['password'])
            user.email = request.form['email']
            user.contact = request.form['contact']
            user.description = request.form['description']
            user.created_date = datetime.date.today()
            user_type = User_Type.query(User_Type.name == 'User').fetch()
            user.type_id = user_type[0].key

            # Add a User detail
            user_detail = User_Detail()
            user_detail.first_name = request.form['first_name']
            user_detail.middle_name = request.form['middle_name']
            user_detail.last_name = request.form['last_name']
            user_detail.location = request.form['location']
            print type(request.form['dob'].encode('ascii', 'ignore'))
            user_detail.dob = datetime.datetime.strptime(request.form['dob'], "%d/%m/%Y").date()
            user_detail_key = user_detail.put()

            # Adding a key in userdetail

            user.detail_id = user_detail_key
            res = user.put()

            if res:
                return jsonify({'id': res.id(), 'message': "Username successfully registered."})
            else:
                return jsonify({'status': 500, 'message': "Error occured"})

    def check_client_token(self, headers):
        if 'CLIENT_TOKEN' in headers:
            jwt_token = headers['CLIENT_TOKEN']
            return check_user_token(jwt_token)

        else:
            return False


class ClientAdditionView(MethodView):
    mail_subject = "Create your Account"
    mail_sender = 'enishpaneru2017@gmail.com'
    link_expiry_period = 99999  # in seconds

    def get(self):
        pass

    def send_mail(self, client_id, client_name, client_email):
        client_token = create_user_token(client_id, self.link_expiry_period)
        account_create_url = "http://127.0.0.1:8080/client/createaccount/" + client_token
        msg_body = "Hello" + client_name + "\n" + "click here to create your account \n" + account_create_url
        new_mail = MailService(self.mail_subject, self.mail_sender, client_email, msg_body)
        result = new_mail.send_mail()
        print "print here"
        print result

    def post(self):
        # add client here
        client_id = 12345  # this should be the newly created client's id
        client_name = "new client"  # this should be the client name
        client_email = request.form['email']
        self.send_mail(client_id, client_name, client_email)

        return "Success"


