import asyncio

from asgiref.sync import sync_to_async
from django.apps import AppConfig


background_tasks = set()


class CoreConfig(AppConfig):
    """
    Currency exchanging core application config.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self) -> None:
        try:
            from core.exchange_rate_providers.utils import initialize_providers

            loop = asyncio.get_running_loop()
            async_initialize_providers = sync_to_async(initialize_providers)
            task = loop.create_task(async_initialize_providers())
            background_tasks.add(task)
            task.add_done_callback(background_tasks.discard)
        except RuntimeError:
            pass
