# start sockets
from threading import Thread
from multiprocessing import Process
from apps.ticketscraping.connection.receiver_process import ReceiverProcess
from apps.ticketscraping.constants import SERVICE_LOCALHOST, ASYNC_TASKS_RECEIVER_PORT


def run_prepare():
   # start receiver socket
   from apps.ticketscraping.connection.mail_receiver import run
   conn_process = Process(target=run, daemon=True)
   conn_process.start()

   # start sender socket
   from apps.ticketscraping.schedulers.mail_scheduler import mail_scheduler
   conn_thread = Thread(target=mail_scheduler.connect)
   conn_thread.start()
   # wait for mailer to connect
   conn_thread.join()

   # start itself
   from apps.ticketscraping.tasks.asynchronous import run_async_tasks
   receiver = ReceiverProcess(run_async_tasks, SERVICE_LOCALHOST, ASYNC_TASKS_RECEIVER_PORT)
   receiver.connect()
   receiver.serve_forever()


def run():
   # starter
   p = Process(target=run_prepare)
   p.start()


if __name__ == '__main__':
   run()
