from google.appengine.ext import ndb


class User_Type(ndb.Model):
    """Model user types."""
    name = ndb.StringProperty()
    permissions=ndb.JsonProperty()