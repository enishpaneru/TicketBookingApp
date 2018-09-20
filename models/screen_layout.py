from google.appengine.ext import ndb


class Screen_Layout(ndb.Model):
    """Model and individual screen_layout for clients."""
    screen_name=ndb.StringProperty()
    client_id=ndb.keyProoperty()
    location=ndb.StringProperty()
    max_rows=ndb.IntegerProperty()
    max_columns=ndb.IntegerProperty()
    seats=ndb.JsonProperty()