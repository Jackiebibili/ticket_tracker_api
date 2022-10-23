import threading
from multiprocessing import Queue
from ..tasks.util.scheduler import Scheduler

def child_process(queue: Queue):
   #TODO
   scheduler = Scheduler('mail scheduler', lambda x: x)
   sched_thread = threading.Thread(target=scheduler.run)
   sched_thread.start()
   while True:
      received_params = queue.get()
      scheduler.enter(*received_params)
