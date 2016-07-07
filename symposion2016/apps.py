from django.apps import AppConfig as BaseAppConfig
from importlib import import_module


class AppConfig(BaseAppConfig):

    name = "symposion2016"

    def ready(self):
        import_module("symposion2016.receivers")
