from google.appengine.ext import ndb
from flask.views import MethodView
from flask import jsonify, request
from models.show import Show
from models.category import Category
from models.price import Price
from datetime import datetime
import json

class ShowAddView(MethodView):
    def get(self):
        show = ndb.Key('Show', 4679521487814656)
        return str((show.get().seats))
        pass

    def post(self):
        show = Show()
        # show.key=ndb.Key('Show', int(request.json['id']))
        show.event_id = ndb.Key('Event', int(request.json['event_id']))
        # We will have a user ID fetch client id from user ID.
        show.client_id = ndb.Key('Client', int(request.json['client_id']))
        show.screen_id = ndb.Key('Screen_Layout', int(request.json['screen_id']))
        show.name = request.json['name']
        show.datetime=datetime.strptime(request.json['datetime'], "%Y-%m-%d %I:%M %p")
        screen = ndb.Key('Screen_Layout', int(request.json['screen_id']))
        seats = screen.get().seats
        print type(seats)
        updated_seats = {}
        for each in seats:
            updated_seats[str(each['row'])+'-'+str(each['column'])]= {'status':4}
        show.seats = updated_seats
        
        categories_price=request.json['category-price']
        
        # Creating a price for each request
        try:
            for each in categories_price:
                price=Price(show_id=show.screen_id, category_id=ndb.Key('Category', each['category']), amount=each['price'])
                price.put()
            res = show.put()
        except :
            return jsonify({"code":500, "message":"server error"})
        
        return jsonify({"code": 200, "id": res.id(), "message": "Success"})




class ShowUpdateView(MethodView):
    def get(self):
        show = ndb.Key('Show', 4679521487814656)
        return str((show.get().seats))
        pass

    def post(self):
        show = Show.get_by_id(request.json['id'])
        if not show:
                return jsonify({"code":404, "message":"Show Not found."})   
        # user=request.environ['USER_ID'].get()
        client_id=ndb.Key('Client',request.json['client_id'])
        # Check if the user is authorized to edit.
        if client_id!=show.client_id:
            return jsonify({"code": 400,  "message": "Not authorized."})
        # UPDATE EXISTING DATA MINOR INFORMATIONS
        show.event_id = ndb.Key('Event', int(request.json['event_id']))
        show.screen_id = ndb.Key('Screen_Layout', int(request.json['screen_id']))
        show.name = request.json['name']
        show.datetime=datetime.strptime(request.json['datetime'], "%Y-%m-%d %I:%M %p")
        res=show.put()
                
        return jsonify({"code": 200, "id": res.id(), "message": "Success"})







# Delete request for shows.
def ShowDeleteMethod(id):
            try:
                show=ndb.Key('Show', int(id))
                if show.get()==None:
                    return jsonify({"code":404, "message":"Show Not found."})    
                show.delete()
                return jsonify({"code":200, "message":"Show Successfully deleted."})
            except :
                return jsonify({"code":500, "message":"Server Error."})
    
        