from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from ..storage.storage import insert_one, find_one_and_update
from ..ticketscraping import constants
import json


# Create your views here.
def subscribe_tm_event_price_tracking(req: HttpRequest):
   if req.method == 'POST':
      body = json.loads(req.body)
      # validation
      for key in ['name', 'price_range', 'ticket_num', 'tm_event_id']:
         if key not in body:
            return HttpResponse('Request is invalid.', status=400)
      doc = {
         "name": body["name"],
         "price_range": body["price_range"],
         "ticket_num": body["ticket_num"],
         "tm_event_id": body["tm_event_id"]
      }
      insert_one(constants.DATABASE['EVENTS'], doc)
      return HttpResponse('OK', status=200)

def unsubscribe_tm_event_price_tracking(req: HttpRequest):
   if req.method == 'POST':
      body = json.loads(req.body)
      # validation
      id = body['subscription_id']
      if not id:
         return HttpResponse('Request is invalid.', status=400)
      res = find_one_and_update(constants.DATABASE['EVENTS'], {"_id": id}, {'$set': {'markPaused': True, }})
      if res:
         return HttpResponse('OK', status=200)
      else:
         return HttpResponse('Subscription id not found.', status=400)
