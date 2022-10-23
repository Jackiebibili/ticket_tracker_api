import threading
from multiprocessing import Process, Queue
from .async_tasks_child_process import child_process

class SchedulerProcess:
   def __init__(self):
      self.queue = Queue()
      self.started = False
      self.starter_thread = None

   def generate_child_process(self):
      cp = Process(target=child_process, args=(self.queue,))
      cp.start()
      self.started = True
      cp.join()

   def start(self):
      self.starter_thread = threading.Thread(
          target=self.generate_child_process)
      self.starter_thread.start()

   def produce(self, *args):
      if not self.started:
         return
      self.queue.put(args)
