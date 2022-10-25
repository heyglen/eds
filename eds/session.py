import contextlib

import requests

from .eds import Eds, PriceArea


@contextlib.contextmanager
def Session(price_area=PriceArea.east_of_great_belt):  # noqa: N802
    with requests.Session() as session:
        yield Eds(session=session, price_area=price_area)
