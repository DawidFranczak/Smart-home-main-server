import os

from django.apps import AppConfig


class RplConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rpl"

    def ready(self) -> None:
        if os.environ.get("RUN_MAIN") == "true":
            from threading import Thread

            from .thread import listener

            thread = Thread(target=listener)
            thread.daemon = True
            thread.start()
