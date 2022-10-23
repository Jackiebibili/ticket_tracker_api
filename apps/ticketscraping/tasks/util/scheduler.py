import time
from sched import scheduler

class Scheduler:
   def __init__(self, name: str, action):
      self.name = name
      self.scheduler = scheduler(time.time, time.sleep)
      self.action = action
   
   def enter(self, *args, **kwargs):
      return self.scheduler.enter(0, 1, self.action, args, kwargs)

   def run(self):
      self.scheduler.run()
