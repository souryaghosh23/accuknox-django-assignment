from django.apps import AppConfig


class DemoappConfig(AppConfig):
    name = "demoapp"
    
class DemoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'demoapp'

    def ready(self):
        from . import signals  # noqa
