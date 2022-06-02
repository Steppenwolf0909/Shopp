import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'config.settings')
from celery import Celery

app = Celery('celery')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(name="send_db_mail")
def send_async_db_mail(templ, recipient, context):
    from dbmail import send_db_mail
    send_db_mail(templ, recipient, context, use_celery=False)
