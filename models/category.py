from google.appengine.ext import ndb


class Category(ndb.Model):
    """Model categories of seat."""
    category_name=ndb.StringProperty()
    screen_id=ndb.KeyProperty()
    seats=ndb.JsonProperty()