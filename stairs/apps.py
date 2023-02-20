from django.apps import AppConfig


class StairsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stairs'

    def ready(self) -> None:
        import stairs.signals
