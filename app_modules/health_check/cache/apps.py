# -*- coding: utf-8 -*-
from django.apps import AppConfig

from app_modules.health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'app_modules.health_check.cache'

    def ready(self):
        from .backends import CacheBackend
        plugin_dir.register(CacheBackend)
