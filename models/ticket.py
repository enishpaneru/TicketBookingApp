from google.appengine.ext import ndb


class Ticket(ndb.Model):
    user_id = ndb.KeyProperty()
    show_id = ndb.KeyProperty()
    seats = ndb.JsonProperty()
    issued_datetime = ndb.DateTimeProperty()
    total_price = ndb.IntegerProperty()
