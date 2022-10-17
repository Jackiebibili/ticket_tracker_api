from apps.ticketscraping.connection.receiver_process import ReceiverProcess
from apps.pushnotification.smtp import send_email, auth_server
from apps.ticketscraping.constants import SERVICE_LOCALHOST, MAIL_RECEIVER_PORT

def run():
   # start itself
   auth_server()
   receiver = ReceiverProcess(send_email, SERVICE_LOCALHOST, MAIL_RECEIVER_PORT)
   receiver.connect()
   receiver.serve_forever()

if __name__ == '__main__':
   run()
