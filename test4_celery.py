from test3_celery import recv_task
from basicutils.socketutils import *
res = recv_task.delay(CoreEntity.wrap_strchain('#C 3 3').json())
print(res.get(timeout=1))
print(res.forget())