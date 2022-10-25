from .receiver import Receiver

class ReceiverProcess(Receiver):
   def __init__(self, action, hostname: str, port: int):
      super().__init__(hostname, port)
      self.action = action

   def serve_forever(self):
      while True:
         res = self.recv()
         self.action(*res)
