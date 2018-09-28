from google.appengine.ext import ndb


class User(ndb.Model):
    """Model an user."""
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()
    contact = ndb.IntegerProperty()
    description = ndb.StringProperty()
    created_date=ndb.DateTimeProperty()
    last_login=ndb.DateTimeProperty()
    type_id=ndb.KeyProperty()
    detail_id=ndb.KeyProperty()


