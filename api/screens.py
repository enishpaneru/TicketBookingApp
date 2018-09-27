from google.appengine.ext import ndb
from flask.views import MethodView
from flask import jsonify, request
from models.screen_layout import Screen_Layout
from models.category import Category
from models.price import Price
import json


class ScreenAddView(MethodView):
    def get(self):
        pass

    def post(self):
        screen = Screen_Layout()
        screen.name = request.json['name']
        screen.client_id = ndb.Key('Client', request.json['client_id'])    # Later this is to be changed from value from token
        screen.location = request.json['location']
        screen.max_rows = request.json['max_rows']
        screen.max_columns = request.json['max_columns']
        res=screen.put()
        print res
        
        seats=[]    #All the seats from categories needs to be added to the database.
        # Fetch seat categories
        categories=request.json['categories']
        print categories
        try:
            for each in categories:
                category=Category()
                category.screen_id=res
                category.name=each['name']
                category.seats=each['seats']
                map( lambda seat: seats.append(seat), each['seats'])
                category.put()  # Create categories for seat for a particular screen.
            screen=res.get()    # Adding seats for the screen fetched from categories
            screen.seats=seats
            res=screen.put()
            return jsonify({"code": 200, "id":res.id(), "message": "Success"})
        except:
            return jsonify({"code":500, "message":"server error"})


class ScreenUpdateView(MethodView):
    def get(self):
        pass
    
    def post(self):
        print request.json['id']
        screen = Screen_Layout.get_by_id(request.json['id'])
        screen.name = request.json['name']
        client_id=screen.client_id.id()
        print client_id
        if client_id!=request.json['client_id']:    # Later this is to be changed with token.
            return jsonify({"code": 404,  "message": "Not authorized."})
        screen.location = request.json['location']
        
        prev_rows=screen.max_rows
        prev_cols=screen.max_columns


        
        if prev_rows!=request.json['max_rows'] or prev_cols!=request.json['max_columns']:
            screen.max_rows = request.json['max_rows']
            screen.max_columns = request.json['max_columns']
            # Deleting the categories of a seat after changing the screen structure.
            options=ndb.QueryOptions(keys_only=True)
            prev_categories=Category.query().filter(Category.screen_id==ndb.Key('Screen_Layout',request.json['id'])).fetch(options=options)
            ndb.delete_multi(prev_categories)
            # We should add the new seat list for new seat grid and new categories for the updated Layout..
            seats=[]
            categories=request.json['categories']
            print categories
            try:
                for each in categories:
                    category=Category()
                    category.screen_id=ndb.Key('Screen',request.json['id'])
                    category.name=each['name']
                    category.seats=each['seats']
                    map( lambda seat: seats.append(seat), each['seats'])
                    category.put()  # Create categories for seat for a particular screen.
                # Adding seats for the screen fetched from categories
                screen.seats=seats
                res=screen.put()
                return jsonify({"code": 200, "id":res.id(), "message": "Success changed layout and other informations."})
            except:
                return jsonify({"code":500, "message":"server error"})
        return jsonify({"code": 200,  "message": "Success changed some minor informations."})



def ScreenDeleteMethod(id):
            try:
                screen=ndb.Key('Screen_Layout', id)
                if not screen:
                    return jsonify({"code":200, "message":"Screen Not found."})    
                screen.delete()
                return jsonify({"code":200, "message":"Screen Successfully deleted."})
            except :
                return jsonify({"code":500, "message":"Server Error."})
    



# class ScreenDeleteView(MethodView):


        

