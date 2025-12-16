import datetime
import os
from typing import Callable

from aiohttp.client import _RequestContextManager
from yarl import URL

from common.utils.networking import get_session


class CurrencyBeaconProvider:
    NAME = 'Currency Beacon'
    PRIORITY = 10

    def __init__(self) -> None:
        self._client = None

    async def get_exchange_rate(
        self,
        source_currency: str,
        exchanged_currency: str,
        valuation_date: datetime.date,
    ) -> float | None:
        response_data = await self.client.retrieve_timeseries(
            source_currency,
            [exchanged_currency],
            valuation_date,
            valuation_date,
        )
        valuation_date_str = valuation_date.strftime(self.client.DATE_FORMAT)
        return response_data.get('response', {}).get(valuation_date_str, {}).get(exchanged_currency)

    @property
    def client(self) -> 'CurrencyBeaconClient':
        if self._client is None:
            self._client = CurrencyBeaconClient()
        return self._client


class CurrencyBeaconClient:
    BASE_URL = 'https://api.currencybeacon.com/'
    CONVERT_ENDPOINT = 'v1/convert'
    TIMESERIES_ENDPOINT = 'v1/timeseries'

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self) -> None:
        self._api_key = os.environ.get('CURRENCY_BEACON_API_KEY', '')

    async def get(self, url: str | URL, **kwargs) -> _RequestContextManager:
        """
        Make GET request.
        """
        session = await get_session()

        return self._make_request(url, session.get, **kwargs)

    def _make_request(  # noqa, pylint: disable=too-many-arguments
        self,
        url: str | URL,
        request_function: Callable,
        headers: dict | None = None,
        **kwargs,
    ) -> _RequestContextManager:
        """
        Make API request.

        Mix in default headers.
        """
        _headers = self._build_request_headers(headers)

        return request_function(url, headers=_headers, **kwargs)

    def _build_request_headers(self, original_headers: dict | None) -> dict:
        """
        Build the dictionary with request headers.

        Combine original headers with CurrencyBeacon authorization headers.
        """
        headers = original_headers.copy() if original_headers is not None else {}

        headers['Authorization'] = f'Bearer {self._api_key}'

        return headers

    async def retrieve_timeseries(
        self,
        source_currency: str,
        exchanged_currencies: list[str],
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> dict:
        url = URL(self.BASE_URL) / self.TIMESERIES_ENDPOINT
        url = url.with_query({
            'base': source_currency,
            'symbols': exchanged_currencies,
            'start_date': start_date.strftime(self.DATE_FORMAT),
            'end_date': end_date.strftime(self.DATE_FORMAT),
        })

        response_context_manager = await self.get(url)
        async with response_context_manager as response:
            return await response.json()
