from google.appengine.ext import ndb
from flask.views import MethodView
from flask import jsonify, request
from models.user import User
from models.user_type import User_Type
from models.user_detail import User_Detail
from models.event import Event
from models.client import Client
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from Mail import MailService
from middlewares.UserAuthentication import create_user_token, check_user_token
from models.screen_layout import Screen_Layout
from models.category import Category
from models.show import Show


class ClientRegisterView(MethodView):
    def get(self):
        pass

    def post(self):
        print "hello"
        query = User.query(User.username == request.json['username']).fetch()

        if query:
            return jsonify({"status":409,'id': query[0].username, 'message': "Username Exists please use another username"})
        else:

            # check the association and validity of the client create account token
            client_id = self.check_client_token(request.headers)
            query_client = User.query(User.detail_id == ndb.Key(Client, client_id)).fetch()

            if not client_id or query_client:
                return jsonify(
                    {"status": 401,
                     'message': "Token validation gone wrong please request a new registration link from the admins"})

            # Add user credentials and minor info
            print client_id
            user = User()
            user.username = request.json['username']
            user.password = generate_password_hash(request.json['password'])
            user.email = request.json['email']
            user.contact = int(request.json['contact'])
            user.description = request.json['description']
            user.created_date = datetime.datetime.today()
            user_type = User_Type.query(User_Type.name == 'Client').get()
            user.type_id = user_type.key

            user.detail_id = ndb.Key(Client, client_id)
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
        account_create_url = "https://ticketbooking-12.firebaseapp.com/register/client/" + client_token
        msg_body = "Hello" + client_name + "\n" + "click here to create your account \n" + account_create_url
        new_mail = MailService(self.mail_subject, self.mail_sender, client_email, msg_body)
        result = new_mail.send_mail()
        print result

    def post(self):
        # add client here
        print request.json
        new_client = Client(name=request.json['name'], description=request.json['description'])
        client_key = new_client.put()
        client_id = client_key.id()  # this should be the newly created client's id
        client_name = new_client.name  # this should be the client name
        client_email = request.json['email']
        self.send_mail(client_id, client_name, client_email)
        print "all ok"
        return jsonify({'status': 'success'})


class ListClientEvent(MethodView):
    def get(self):
        user_id = request.environ['USER_ID']
        print "###"
        print request.environ['USER_ID']
        client_id = user_id.get().detail_id
        events = Event.query(Event.client_id == client_id).fetch()
        events_list = []
        for event in events:
            events_list.append({"id": event.key.id(), "name": event.name, "duration": event.duration,
                                "description": event.description})
        return jsonify(events_list)


class ListClientScreens(MethodView):
    def get(self):
        user_id = request.environ['USER_ID']
        client_id = user_id.get().detail_id
        screens = Screen_Layout.query(Screen_Layout.client_id == client_id).fetch()
        screen_list = []
        for screen in screens:
            screen_list.append({"id": screen.key.id(), "name": screen.name, "location": screen.location})
        return jsonify(screen_list)


class ListClientScreenCategory(MethodView):
    def get(self, screen_id):
        screen_id = ndb.Key(Screen_Layout, int(screen_id))
        categories = Category.query(Category.screen_id == screen_id).fetch()

        category_list = []
        for category in categories:
            category_list.append({"id": category.key.id(), 'name': category.name})
        return jsonify(category_list)


class ListClientShows(MethodView):
    def get(self):
        user_id = request.environ['USER_ID']
        client_id = user_id.get().detail_id
        shows = Show.query(Show.client_id == client_id)
        shows_list = []
        for show in shows:
            event_name = show.event_id.get().name
            screen_name = show.screen_id.get().name
            shows_list.append({"event_name": event_name, 'screen_name': screen_name, "datetime": show.datetime})
        return jsonify(shows_list)


class ClientDetail(MethodView):
    def get(self):
        user_id = request.environ['USER_ID']
        user = user_id.get()
        client = user.detail_id.get()

        user_name = user.username
        email = user.email
        contact = user.contact
        description = user.description

        client_name = client.name
        client_description = client.description

        return jsonify({'user_name': user_name, 'email': email, 'contact': contact, 'description': description,
                        'client_name': client_name, 'client_description': client_description})
