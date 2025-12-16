from ordered_model.models import OrderedModelQuerySet


class ExchangeRateProviderConfigQuerySet(OrderedModelQuerySet):
    def active(self) -> 'ExchangeRateProviderConfigQuerySet[ExchangeRateProviderConfig]':
        return self.filter(is_active=True)
