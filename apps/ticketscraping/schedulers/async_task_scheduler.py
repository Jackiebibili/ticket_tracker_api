from .scheduler_process import SchedulerProcess

print(__name__)
async_tasks_scheduler = SchedulerProcess()
async_tasks_scheduler.start()
