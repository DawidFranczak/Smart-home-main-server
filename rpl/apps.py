from django.apps import AppConfig


class RplConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rpl'

    def ready(self):
        import rpl.signals
