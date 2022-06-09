from django.apps import AppConfig
from utils import get_db_handle
from ticketscraping.scraping import start
from datetime import datetime

class MyAppConfig(AppConfig):
   name = "tmtracker"
   verbose_name = "start tmtracker"
   
   def ready(self):
      print(f"server started at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
      print("=== database connection is established ===")
      start()
