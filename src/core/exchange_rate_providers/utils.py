import logging
from functools import lru_cache
from importlib.metadata import entry_points

from django.core.management import call_command
from django.db import transaction

from core.exchange_rate_providers.typing import ExchangeRateProvider
from core.models import ExchangeRateProviderConfig

PROVIDERS_GROUP = 'my_currency.provider'


logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def get_providers():
    providers = []

    for entry_point in entry_points(group=PROVIDERS_GROUP):
        try:
            providers.append(entry_point.load())
        except Exception:
            logger.warning(
                f'An unexpected error during provider entrypoint "{entry_point.name} = {entry_point.value}" '
                f'processing. Skipped.'
            )

    valid_providers = {}

    for provider in providers:
        if not isinstance(provider, ExchangeRateProvider):
            logger.warning(f'{provider.__name__} does not support the exchange rate provider protocol. Skipped.')
            continue

        provider_name = provider.NAME
        if provider_name in valid_providers:
            logger.warning(f'The provider with name "{provider_name}" was already loaded. Skipped.')
            continue

        valid_providers[provider_name] = provider

    return valid_providers


def initialize_providers():
    providers = get_providers()

    provider_configs = {config.provider: config for config in ExchangeRateProviderConfig.objects.all()}
    if len(providers) != len(provider_configs) or list(providers.keys()) != list(provider_configs.keys()):
        deactivated_provider_names = {config.provider for config in provider_configs.values() if not config.is_active}

        with transaction.atomic():
            ExchangeRateProviderConfig.objects.all().delete()
            ExchangeRateProviderConfig.objects.bulk_create([
                ExchangeRateProviderConfig(
                    provider=name,
                    order=provider.PRIORITY,
                    is_active=name not in deactivated_provider_names,
                )
                for name, provider in providers.items()
            ])

        call_command('reorder_model', 'core.ExchangeRateProviderConfig')
