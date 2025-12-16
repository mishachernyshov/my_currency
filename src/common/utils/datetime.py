from datetime import date, timedelta
from typing import Generator


def date_range(start: date, end: date) -> Generator[date, None, None]:
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)
