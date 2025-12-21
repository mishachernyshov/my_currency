import asyncio
from collections import defaultdict
from decimal import Decimal

from django.utils import timezone

from common.utils.datetime import date_range
from common.utils.iterators import paginate_stream
from core.exchange_rate_providers.utils import get_providers
from core.models import Currency, CurrencyExchangeRate, ExchangeRateProviderConfig

CONCURRENT_EXCHANGE_RATES_REQUESTS_LIMIT = 50
DATE_FORMAT = '%Y-%m-%d'


async def get_currency_rates(source_currency, date_from, date_to):
    source_currency_code = source_currency.code
    exchanged_currencies = {
        record.code: record async for record in Currency.objects.exclude(code=source_currency_code)
    }
    start_to_end_date_range = date_range(date_from, date_to)
    dates_processing_page_size = (
        max(CONCURRENT_EXCHANGE_RATES_REQUESTS_LIMIT // len(exchanged_currencies), 1)
        if exchanged_currencies else 1
    )
    results = defaultdict(dict)

    for dates in paginate_stream(start_to_end_date_range, page_size=dates_processing_page_size):
        date_currency_pairs = [
            (date, exchanged_currency)
            for date in dates for exchanged_currency in exchanged_currencies
        ]
        date_exchange_rates = await asyncio.gather(*[
            get_date_exchange_rate(source_currency_code, exchanged_currency, date)
            for date, exchanged_currency in date_currency_pairs
        ])
        currency_exchange_rates = []

        for date_currency_pair, exchange_rate in zip(date_currency_pairs, date_exchange_rates):
            date, exchanged_currency = date_currency_pair
            formatted_date = date.strftime(DATE_FORMAT)
            results[formatted_date][exchanged_currency] = exchange_rate

            if exchange_rate:
                currency_exchange_rates.append(CurrencyExchangeRate(
                    source_currency=source_currency,
                    exchanged_currency=exchanged_currencies[exchanged_currency],
                    valuation_date=date,
                    rate_value=exchange_rate,
                ))

        await CurrencyExchangeRate.objects.abulk_create(
            currency_exchange_rates,
            update_conflicts=True,
            update_fields=['rate_value'],
            unique_fields=['source_currency', 'exchanged_currency', 'valuation_date'],
        )

    return results


async def convert_amount(source_currency, exchanged_currency, amount) -> float | None:
    today = timezone.now().date()
    exchange_rate = await get_date_exchange_rate(source_currency.code, exchanged_currency.code, today)

    if exchange_rate:
        await CurrencyExchangeRate.objects.aget_or_create(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=today,
            rate_value=exchange_rate,
        )

    return Decimal(exchange_rate) * amount if exchange_rate else None


async def get_date_exchange_rate(source_currency_code, exchanged_currency_code, date):
    try:
        currency_exchange_rate = await CurrencyExchangeRate.objects.aget(
            source_currency__code=source_currency_code,
            exchanged_currency__code=exchanged_currency_code,
            valuation_date=date,
        )
    except CurrencyExchangeRate.DoesNotExist:
        pass
    else:
        return currency_exchange_rate.rate_value

    providers = get_providers()
    prioritized_provider_configs = ExchangeRateProviderConfig.objects.active()

    async for provider_config in prioritized_provider_configs:
        provider = providers[provider_config.provider]
        exchange_rate = await get_exchange_rate_data(source_currency_code, exchanged_currency_code, date, provider)

        if exchange_rate is None:
            continue

        return exchange_rate
    return None


async def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider):
    return await provider().get_exchange_rate(source_currency, exchanged_currency, valuation_date)
