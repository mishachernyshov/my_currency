import random


class MockProvider:
    NAME = 'Mock'
    PRIORITY = 1

    async def get_exchange_rate(self, *args, **kwargs) -> float | None:
        return random.random()
