import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class ExchangeRateProvider(Protocol):
    NAME: str
    PRIORITY: int

    async def get_exchange_rate(
        self,
        source_currency: str,
        exchanged_currency: str,
        valuation_date: datetime.date,
    ) -> float | None:
        pass
