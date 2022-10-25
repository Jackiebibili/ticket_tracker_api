import time
from sched import scheduler
from ...constants import AWAKE_SCHEDULER_INTERVAL

class Scheduler:
   def __init__(self, name: str, action):
      self.name = name
      self.scheduler = scheduler(time.time, time.sleep)
      self.awake_scheduler = scheduler(time.time, time.sleep)
      self.action = action
   
   def enter(self, *args, **kwargs):
      return self.scheduler.enter(0, 1, self.action, args, kwargs)

   def iter_awake_scheduler(self):
      # awake the main scheduler
      self.scheduler.run() # blocking
      self.awake_scheduler.enter(
          AWAKE_SCHEDULER_INTERVAL, 1, self.iter_awake_scheduler)
   
   def run(self):
      self.iter_awake_scheduler()
      self.awake_scheduler.run()
