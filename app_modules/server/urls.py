# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import ServerHealthCheck, RabbitMQServerHealthChaeck

urlpatterns = [
    url(r'^$', ServerHealthCheck.as_view(), name='server_check_home'),
    url(r'^rabbit-mq-server/$', RabbitMQServerHealthChaeck.as_view(), name='rabbit_server_check_home'),
]
