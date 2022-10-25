from multiprocessing.connection import Client
from threading import Semaphore

class Receiver:
   def __init__(self, hostname: str, port: int):
      self.lock = Semaphore(1)
      self.hostname = hostname
      self.port = port
      self.conn = None

   def connect(self):
      self.conn = Client(address=(self.hostname, self.port,))

   def recv(self):
      if self.conn is None:
         raise Exception('connection is not established')
      self.lock.acquire()
      res = self.conn.recv()
      self.lock.release()
      return res

   def __del__(self):
      if self.conn is not None: self.conn.close()

