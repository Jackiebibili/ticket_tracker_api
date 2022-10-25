from ..connection.sender import Sender
from ..constants import SERVICE_LOCALHOST, MAIL_RECEIVER_PORT


mail_scheduler = Sender(SERVICE_LOCALHOST, MAIL_RECEIVER_PORT)
