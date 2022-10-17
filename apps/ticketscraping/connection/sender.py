from multiprocessing.connection import Listener
from threading import Semaphore

class Sender:
   def __init__(self, hostname: str, port: int):
      self.lock = Semaphore(1)
      self.hostname = hostname
      self.port = port
      self.conn = None

   def connect(self):
      listener = Listener(address=(self.hostname, self.port))
      self.conn = listener.accept()
      print("conn accepted ", self.port)

   def send(self, *args):
      if self.conn is None:
         raise Exception('connection is not established')
      self.lock.acquire()
      self.conn.send(args)
      self.lock.release()
      return True

   def __del__(self):
      if self.conn is not None:
         self.conn.close()
