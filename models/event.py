from google.appengine.ext import ndb


class Event(ndb.Model):
    name = ndb.StringProperty()
    client_id = ndb.KeyProperty()
    description = ndb.StringProperty()
