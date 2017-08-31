from __future__ import absolute_import, unicode_literals

from celery.task import Task
from django.conf import settings


class TestTask(Task):
    name = 'app_modules.server.test_task'
    routing_key = 'app_modules.server.test_task'
    ignore_result = True
    default_retry_delay = settings.DEFAULT_CELERY_RETRY_DELAY
    max_retries = settings.DEFAULT_CELERY_MAX_RETRIES

    def run(self, test='Text goes here'):
        print test
