from celery import Celery

def make_celery(app_name=__name__):
    redis_uri = 'amqp://localhost//'
    return Celery(app_name, backend='redis://localhost:6379', broker=redis_uri)

def init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask


