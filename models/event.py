from google.appengine.ext import ndb


class Event(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    active_shows_id = ndb.JsonProperty()

