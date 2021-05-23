from flask import Response, redirect, request, url_for
from typing import Optional
from http import HTTPStatus
from celery import Celery

def make_celery(app_name=__name__):
    redis_uri = 'redis://0.0.0.0:6379'
    return Celery(app_name, backend=redis_uri, broker=redis_uri)

def init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask


def https_redirect() -> Optional[Response]:
    if request.scheme == 'http':
        return redirect(url_for(request.endpoint,
                                _scheme='https',
                                _external=True),
                        HTTPStatus.PERMANENT_REDIRECT)
