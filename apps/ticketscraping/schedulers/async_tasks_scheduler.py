from ..connection.sender import Sender
from ..constants import SERVICE_LOCALHOST, ASYNC_TASKS_RECEIVER_PORT

async_tasks_scheduler = Sender(SERVICE_LOCALHOST, ASYNC_TASKS_RECEIVER_PORT)
