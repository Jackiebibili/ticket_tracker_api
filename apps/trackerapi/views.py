from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from ..storage.storage import insert_one, find_one_and_update
from .error_handler import BadRequestException, wrap_error_handler
from ..ticketscraping import constants
import json


# Create your views here.
@wrap_error_handler
def subscribe_tm_event_price_tracking(req: HttpRequest):
   if req.method == 'POST':
      body = json.loads(req.body)
      # validation
      for key in constants.SUBSCRIBE_REQUEST_PROPS.values():
         if key not in body:
            raise BadRequestException('Request is invalid.')
      # validation
      target_price = body["target_price"]
      tolerance = body["tolerance"]
      if target_price - tolerance < 0:
         raise BadRequestException('Lowest price cannot be negative.')

      doc = constants.filter_obj_from_attrs(body, constants.SUBSCRIBE_REQUEST_PROPS)

      insert_one(constants.DATABASE['EVENTS'], doc)
      return HttpResponse('OK', status=200)


@wrap_error_handler
def unsubscribe_tm_event_price_tracking(req: HttpRequest):
   if req.method == 'POST':
      body = json.loads(req.body)
      id = body['subscription_id']

      res = find_one_and_update(constants.DATABASE['EVENTS'], {"_id": id}, {'$set': {'markPaused': True}})
      if res:
         return HttpResponse('OK', status=200)
      else:
         raise BadRequestException('Subscription id not found.')
