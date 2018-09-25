from google.appengine.ext import ndb


class User(ndb.Model):
    """Model an user."""
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()
    contact = ndb.StringProperty()
    description = ndb.StringProperty()
    created_date=ndb.DateProperty()
    last_login=ndb.DateTimeProperty()
    type_id=ndb.KeyProperty()
    detail_id=ndb.KeyProperty()


