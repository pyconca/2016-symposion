from django.apps import AppConfig as BaseAppConfig
from importlib import import_module


class AppConfig(BaseAppConfig):

    name = "symposion_test"

    def ready(self):
        import_module("symposion_test.receivers")
