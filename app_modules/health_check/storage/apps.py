# -*- coding: utf-8 -*-
from django.apps import AppConfig

from app_modules.health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'app_modules.health_check.storage'

    def ready(self):
        from .backends import DefaultFileStorageHealthCheck
        plugin_dir.register(DefaultFileStorageHealthCheck)
