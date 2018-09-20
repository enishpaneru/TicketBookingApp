from google.appengine.ext import ndb


class Client(ndb.Model):
    """Model and individual client."""
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    screen_list_id = ndb.JsonProperty()
