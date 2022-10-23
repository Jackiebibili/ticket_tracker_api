from apps.ticketscraping.scraping import start
from datetime import datetime
from threading import Thread
from multiprocessing import Process

def run():
   print(
       f"ticket scraping service started at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
   # start scraping
   start()

if __name__ == '__main__':
    p = Process(target=run)
    p.start()
    p.join()