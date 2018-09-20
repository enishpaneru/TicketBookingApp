from google.appengine.ext import ndb


class Client(ndb.Model):
    """Model and individual client."""
    client_name=ndb.StringProperty()
    client_description=ndb.StringProperty()
    screen_list_id=ndb.JsonProperty()