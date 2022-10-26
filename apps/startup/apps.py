from django.apps import AppConfig
from datetime import datetime
from threading import Thread
from multiprocessing import Process


def run_prepare():
    # import module inside the child process to prevent execution in the parent process
    print(
        f"ticket scraping service started at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # start sender socket
    from apps.ticketscraping.schedulers.async_tasks_scheduler import async_tasks_scheduler
    conn_thread = Thread(target=async_tasks_scheduler.connect)
    conn_thread.start()
    # wait for async tasks handler to connect
    conn_thread.join()

    # start itself (scraping)
    from apps.ticketscraping.scraping import start
    start()


def run():
    # starter
    p = Process(target=run_prepare, daemon=True)
    p.start()
    # start receiver socket
    from apps.ticketscraping.connection.asyn_tasks_receiver import run
    conn_process = Process(target=run)
    conn_process.start()


class MyAppConfig(AppConfig):
   name = "apps.startup"
   verbose_name = "start tmtracker"

   def ready(self):
        run()
