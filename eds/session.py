import contextlib
from typing import AsyncIterator

import aiohttp

from .eds import Eds, PriceArea


@contextlib.asynccontextmanager
async def Session(  # noqa: N802
    price_area=PriceArea.east_of_great_belt,
) -> AsyncIterator[Eds]:  # noqa: N802
    async with aiohttp.ClientSession() as session:
        yield Eds(session=session, price_area=price_area)
