from django.db import models
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModel

from core.managers import ExchangeRateProviderConfigManager


class Currency(models.Model):
    """
    Represents the currency.
    """

    code = models.CharField(max_length=3, unique=True, verbose_name=_('Code'))
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    symbol = models.CharField(max_length=10, verbose_name=_('Symbol'))

    def __str__(self) -> str:
        return f'{self.name} ({self.code})'

    class Meta:
        indexes = [
            models.Index(fields=('code',)),
        ]
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')


class CurrencyExchangeRate(models.Model):
    """
    Represents the currency exchange rate for a specific day.
    """

    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField()
    rate_value = models.DecimalField(decimal_places=6, max_digits=18)

    def __str__(self) -> str:
        return f'{self.source_currency.code} → ({self.exchanged_currency.code})'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['source_currency', 'exchanged_currency', 'valuation_date'],
                name='unique_currency_pair_date',
            )
        ]
        verbose_name = _('Currency exchange rate')
        verbose_name_plural = _('Currency exchange rates')


class ExchangeRateProviderConfig(OrderedModel):
    """
    Configuration of the exchange rate provider.
    """

    provider = models.CharField(max_length=128, verbose_name=_('Provider'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))

    objects = ExchangeRateProviderConfigManager()

    def __str__(self) -> str:
        return f'{self.provider} ({self.order}) {"✔" if self.is_active else "✘"}'

    class Meta(OrderedModel.Meta):
        verbose_name = _('Exchange rate provider configuration')
        verbose_name_plural = _("Exchange rate providers' configurations")
