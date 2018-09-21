from google.appengine.ext import ndb


class Category(ndb.Model):
    """Model categories of seat."""
    name = ndb.StringProperty()
    screen_id = ndb.KeyProperty()
    seats = ndb.JsonProperty()
