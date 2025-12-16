from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from core import models


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """
    Provide admin control over Currency model.
    """


@admin.register(models.ExchangeRateProviderConfig)
class ExchangeRateProviderConfigAdmin(OrderedModelAdmin):
    """
    Provide admin control over ExchangeRateProviderConfig model.
    """

    list_display = ('provider', 'is_active', 'order', 'move_up_down_links')
