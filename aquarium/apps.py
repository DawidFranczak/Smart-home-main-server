import os

from django.apps import AppConfig


class AquariumConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aquarium"

    def ready(self) -> None:
        if os.environ.get("RUN_MAIN") == "true":
            from threading import Thread

            from .thread import aquas_check

            thread = Thread(target=aquas_check)
            thread.daemon = True
            thread.start()
