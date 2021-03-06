from django.apps import AppConfig
from ticketscraping.scraping import start
from datetime import datetime
from threading import Thread


class MyAppConfig(AppConfig):
   name = "startupApp"
   verbose_name = "start tmtracker"

   def ready(self):
      print(
          f"server started at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
      print("=== database connection is established ===")
      Thread(target=start).start()
