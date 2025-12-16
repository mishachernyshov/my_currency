from django.urls import path

from core.api.v1.views import ConvertAmountView, CurrencyRatesTimeSeriesView


urlpatterns = [
    path('currency_rates_time_series/', CurrencyRatesTimeSeriesView.as_view(), name='currency_rates_time_series'),
    path('convert/', ConvertAmountView.as_view(), name='convert'),
]
