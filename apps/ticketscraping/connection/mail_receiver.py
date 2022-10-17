from apps.ticketscraping.connection.receiver_process import ReceiverProcess
# from ..tasks.asynchronous import run_async_tasks
from apps.ticketscraping.constants import SERVICE_LOCALHOST, MAIL_RECEIVER_PORT

def run():
   # start itself
   receiver = ReceiverProcess(lambda x: print(
       x), SERVICE_LOCALHOST, MAIL_RECEIVER_PORT)
   receiver.connect()
   receiver.serve_forever()

if __name__ == '__main__':
   run()
