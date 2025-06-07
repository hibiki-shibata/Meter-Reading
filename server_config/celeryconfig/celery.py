import os

from celery import Celery

# Celery config: https://docs.celeryq.dev/en/latest/django/first-steps-with-django.html
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server_config.settings') # This path shoudld be relative path from entry point

app = Celery('celeryconfig')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')