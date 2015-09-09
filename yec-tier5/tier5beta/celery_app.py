from __future__ import absolute_import
import os
from django.conf import settings
from celery import Celery
from kombu import Exchange, Queue

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tier5beta.settings')



CELERY_IGNORE_RESULT = True


BROKER_URL = 'amqp://ljqqgbys:tCXHecSBuGNKFTU7u7apgL6BpAnnnksE@owl.rmq.cloudamqp.com/ljqqgbys'

app = Celery("tasks", broker=BROKER_URL)
app.config_from_object('django.conf:settings')
app.conf.update(CELERY_RESULT_BACKEND='djcelery.backends.database.DatabaseBackend')
app.conf.update(CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# import celery.bin.amqp
# amqp = celery.bin.amqp.amqp(app = app)
# amqp.run('queue.purge', 'default')


CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('for_twitter', Exchange('for_twitter'), routing_key='for_twitter'),
    Queue('send_emails', Exchange('send_emails'), routing_key='send_emails'),
)

