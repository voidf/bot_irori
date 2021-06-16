from multiprocessing.managers import BaseManager
from queue import Queue
queue = Queue(maxsize=100)
class QueueManager(BaseManager): pass
QueueManager.register('get_queue', callable=lambda:queue)
m = QueueManager(address=('localhost', 50000), authkey=b'abracadabra')
m.connect()
queue = m.get_queue()


from dataclasses import dataclass
import random, string

@dataclass
class PendingTask():
    rawstr: str


while 1:
    tp = queue.get()
    print(tp)