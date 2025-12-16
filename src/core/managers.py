from ordered_model.models import OrderedModelManager

from core.querysets import ExchangeRateProviderConfigQuerySet


class ExchangeRateProviderConfigManager(OrderedModelManager):
    def get_queryset(self):
        return ExchangeRateProviderConfigQuerySet(self.model, using=self._db)

    def active(self) -> ExchangeRateProviderConfigQuerySet['ExchangeRateProviderConfig']:
        return self.get_queryset().active()
