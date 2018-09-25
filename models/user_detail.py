from google.appengine.ext import ndb


class User_Detail(ndb.Model):
    """Model and individual user details."""
    first_name = ndb.StringProperty()
    middle_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    location = ndb.StringProperty()
    dob = ndb.DateProperty()
    
    
    

