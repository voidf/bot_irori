from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//',backend="mongodb://127.0.0.1:27017/irori_taskqueue")


@app.task
def add(x, y):
    return x + y