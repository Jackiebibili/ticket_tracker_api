from django.apps import AppConfig
from ..ticketscraping.scraping import start
from datetime import datetime
from threading import Thread


class MyAppConfig(AppConfig):
   name = "apps.startup"
   verbose_name = "start tmtracker"

   def ready(self):
      print(
          f"server started at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
      # start scraping
      Thread(target=start).start()
