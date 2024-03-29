import datetime

from eds.mo import Period


async def test_get(eds, relative_costs):
    total = 0
    for period in await eds.get():
        assert isinstance(period, Period)
        assert isinstance(period.when, datetime.datetime)
        assert period.relative_price in relative_costs
        total += 1
    assert total
