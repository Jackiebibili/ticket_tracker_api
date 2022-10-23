import threading
from multiprocessing import Queue
from ..tasks.util.scheduler import Scheduler
from ..tasks.asynchronous import run_async_tasks

def child_process(queue: Queue):
   scheduler = Scheduler('asynchronous tasks scheduler', run_async_tasks)
   sched_thread = threading.Thread(target=scheduler.run)
   sched_thread.start()
   while True:
      received_params = queue.get()
      scheduler.enter(*received_params)
