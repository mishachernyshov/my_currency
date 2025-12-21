from adrf.routers import DefaultRouter
from django.urls import include, path

from core.api.v1.views import ConvertAmountView, CurrencyRatesTimeSeriesView, CurrencyViewSet


router = DefaultRouter()
router.register('currency', CurrencyViewSet, basename='currency')


urlpatterns = [
    path('currency_rates_time_series/', CurrencyRatesTimeSeriesView.as_view(), name='currency_rates_time_series'),
    path('convert/', ConvertAmountView.as_view(), name='convert'),
    path('', include(router.urls)),
]
