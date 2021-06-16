from multiprocessing.managers import BaseManager
from queue import Queue
queue = Queue()

from dataclasses import dataclass
import random, string

@dataclass
class PendingTask():
    rawstr: str

class QueueManager(BaseManager): pass
QueueManager.register('get_queue', callable=lambda:queue)
m = QueueManager(address=('', 50000), authkey=b'abracadabra')
s = m.get_server()
print('server running...')
s.serve_forever()