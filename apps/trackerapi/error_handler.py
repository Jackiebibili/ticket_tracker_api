from django.http import JsonResponse

# custom exceptions
class BadRequestException(Exception):
   pass

# error handler decorator
def wrap_error_handler(fn):
   def inner_fn(*args, **kwargs):
      try:
         return fn(*args, **kwargs)
      except BadRequestException as ex:
         # bad request
         return JsonResponse({"error": str(ex)}, status=400)
      except Exception as ex:
         # internal server error
         return JsonResponse({"error": "something went wrong."}, status=500)
   return inner_fn