from multiprocessing.managers import BaseManager
from queue import Queue
queue = Queue()
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

def randstr(l: int) -> str: return ''.join(random.choices(string.ascii_letters+string.digits,k=l))

import time

while 1:
    time.sleep(random.random())
    tp = PendingTask(randstr(6))

    print(tp)
    queue.put(tp)