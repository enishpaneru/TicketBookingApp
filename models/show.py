from google.appengine.ext import ndb


class Show(ndb.Model):
    event_id = ndb.KeyProperty()
    client_id = ndb.KeyProperty()
    screen_id = ndb.KeyProperty()
    show_name = ndb.StringProperty()
    datetime = ndb.DateTimeProperty()
    seats = ndb.JsonProperty()
