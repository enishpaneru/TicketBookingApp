from google.appengine.ext import ndb


class Event(ndb.Model):
    client_id = ndb.KeyProperty()
    name = ndb.StringProperty()
    description = ndb.StringProperty()

