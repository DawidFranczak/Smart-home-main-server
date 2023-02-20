from django.apps import AppConfig


class LightConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'light'

    def ready(self):
        import light.signals
