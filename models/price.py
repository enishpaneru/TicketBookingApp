from google.appengine.ext import ndb


class Price(ndb.Model):
    show_id = ndb.KeyProperty()
    category_id = ndb.KeyProperty()
    amount = ndb.IntegerProperty()
