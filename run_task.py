from apps import celery, create_app, init_celery

app = create_app()
init_celery(celery, app)
