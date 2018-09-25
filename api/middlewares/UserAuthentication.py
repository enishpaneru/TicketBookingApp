import fnmatch, datetime
from flask import redirect, url_for
import jwt
from flask import jsonify

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 2000

login_required_paths = ['/events/*/shows/*']
relogin_path = "/events"


class LoggerMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        for path in login_required_paths:
            if fnmatch.fnmatch(environ['PATH_INFO'], path):
                if 'HTTP_USER_TOKEN' in environ:
                    jwt_token = environ['HTTP_USER_TOKEN']
                    try:
                        payload = jwt.decode(jwt_token, JWT_SECRET,
                                             algorithms=[JWT_ALGORITHM])
                        environ['USER_ID'] = payload['user_id']
                    except (jwt.DecodeError, jwt.ExpiredSignatureError):
                        start_response('302 Found', [('Location', relogin_path)])
                        return '1'
                else:
                    start_response('302 Found', [('Location', relogin_path)])
                    return '1'

        return self.app(environ, start_response)


def create_user_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return jwt_token



