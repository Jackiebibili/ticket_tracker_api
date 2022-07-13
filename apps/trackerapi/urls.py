from django.urls import path
from . import views

urlpatterns = [
   path('subscribe/', views.subscribe_tm_event_price_tracking),
   path('unsubscribe/', views.unsubscribe_tm_event_price_tracking)
]