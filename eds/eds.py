"""
Energy Data Service
"""

import datetime
import statistics
from typing import TYPE_CHECKING, List

from .mo import Period, RelativeCost

if TYPE_CHECKING:
    import aiohttp


class PriceArea:
    west_of_great_belt = "DK1"
    east_of_great_belt = "DK2"


class Eds:
    version = "1.0.0"

    def __init__(
        self, session: "aiohttp.ClientSession", price_area=PriceArea.east_of_great_belt
    ):
        self._price_area = price_area
        self._session = session

    async def get(self) -> List[Period]:
        async with self._session.get(
            "https://api.energidataservice.dk/dataset/Elspotprices",
        ) as response:
            data = await response.json()

            periods = list()
            for record in data["records"]:
                price_area = record["PriceArea"]
                if price_area != self._price_area.value:
                    continue
                timestamp = datetime.datetime.strptime(
                    record["HourDK"], "%Y-%m-%dT%H:%M:%S"
                )
                period = Period(
                    when=timestamp,
                    price=round(record["SpotPriceDKK"] / 10),
                )
                periods.append(period)

        cheap, expensive = statistics.quantiles([p.price for p in periods], n=3)

        for period in periods:
            if period.price < cheap:
                period.relative_price = RelativeCost.cheap
            elif cheap <= period.price < expensive:
                period.relative_price = RelativeCost.mid_priced
            elif expensive <= period.price:
                period.relative_price = RelativeCost.expensive

        return periods
