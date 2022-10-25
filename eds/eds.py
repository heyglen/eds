"""
Energy Data Service
"""

import datetime
import enum
import statistics
from typing import List, Optional

import requests

from .mo import Period, RelativeCost


class PriceArea(enum.Enum):
    west_of_great_belt = "DK1"
    east_of_great_belt = "DK2"


def _build_query(
    price_area=PriceArea.east_of_great_belt, when: Optional[datetime.datetime] = None
):
    if when is None:
        when = datetime.datetime.now()
    when_text = when.strftime("%Y-%m-%d")
    where_hour_utc = 'HourUTC: {_gte: "' + when_text + '"}'
    where_price_area = f'PriceArea: {{_eq: "{price_area.value}"}}'
    where = "where: {" + where_hour_utc + where_price_area + "}"
    order_by = "order_by: {HourDK: asc}"
    limit = "limit: 100"
    # HourUTC HourDK PriceArea SpotPriceDKK SpotPriceEUR
    fields = "{HourDK SpotPriceDKK }"
    query = (
        "query Dataset {elspotprices("
        + where
        + " "
        + order_by
        + " "
        + limit
        + " offset: 0) "
        + fields
        + "}"
    )
    return query


class Eds:
    version = "0.2.0"

    def __init__(
        self, session: requests.Session, price_area=PriceArea.east_of_great_belt
    ):
        self._price_area = price_area
        self._session = session

    def get(self) -> List[Period]:
        response = self._session.post(
            "https://data-api.energidataservice.dk/v1/graphql",
            json=dict(
                query=_build_query(
                    price_area=self._price_area,
                )
            ),
        )

        data = response.json()

        periods = list()
        for record in data["data"]["elspotprices"]:
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
                period.relative_price = RelativeCost.normal
            elif expensive <= period.price:
                period.relative_price = RelativeCost.expensive

        return periods
