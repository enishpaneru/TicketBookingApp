import fnmatch, datetime
import jwt
from google.appengine.ext import ndb
from models.user import User
from cgi import parse_qs
from flask_cors import cross_origin

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

login_not_required_paths = ['/', '/events', '/events/[0-999999999999999999999]', '/events/*/shows', '/initdatafeed',
                            '/login',
                            '/postevent',
                            '/postshow',
                            '/postcategory', '/postclient', '/postprice', 'postscreen', 'postscreenman', '/postshowman',
                            '/register/*']


class LoggerMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        if environ['REQUEST_METHOD'] == "OPTIONS":
            return self.app(environ, start_response)

        for path in login_not_required_paths:
            if fnmatch.fnmatch(environ['PATH_INFO'], path):
                print "open path"
                return self.app(environ, start_response)
        print "closed path"
        if 'HTTP_USER_TOKEN' in environ:
            jwt_token = environ['HTTP_USER_TOKEN']
            print "here"
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET,
                                     algorithms=[JWT_ALGORITHM])
                print "##"
                print jwt_token
                print payload['user_id']
                environ['USER_ID'] = ndb.Key(User, int(payload['user_id']))
                # if not check_user_permission(environ['USER_ID'],environ['PATH_INFO']):
                #     start_response('302 Found', [('Location', relogin_path)])
                #     return '1'
                return self.app(environ, start_response)
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                start_response('401 Unauthorized', [])
                return {'code': 401, "message": "User not authorised"}
        else:
            start_response('401 Unauthorized', [])
            return {'code': 401, "message": "User not authorised"}


def create_user_token(user_id, JWT_EXP_DELTA_SECONDS):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return jwt_token


def check_user_token(jwt_token):
    try:
        payload = jwt.decode(jwt_token, JWT_SECRET,
                             algorithms=[JWT_ALGORITHM])
        return int(payload['user_id'])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return False


def check_user_permission(user_id, path):
    user_type_id = user_id.get().user_type
    user_type = user_type_id.get()
    if path in user_type.permissions.values():
        return True
    else:
        return False
