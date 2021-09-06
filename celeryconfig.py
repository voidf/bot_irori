broker_url = 'pyamqp://guest@localhost//'
result_backend= "mongodb://127.0.0.1:27017/irori_taskqueue"

task_time_limit = 30
result_expires = 3600

imports = tuple()
worker_pool_restarts = True