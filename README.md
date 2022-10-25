# Energy Data Service

Command line interface:

```
eds power get
72022.10.25
        02:00  42 øre
        03:00  42 øre
        04:00  50 øre
        05:00  53 øre
        ...
```

API:

```python
import datetime

from eds import Session, RelativeCost, PriceArea

relative_prices = (
    RelativeCost.cheap,
    RelativeCost.normal,
    RelativeCost.expensive,
)

with Session(price_area=PriceArea.east_of_great_belt) as session:
    for period in session.get():
        assert isinstance(period.when, datetime.datetime)
        assert isinstance(period.price, float)
        assert period.currency_unit == "øre"
        assert period.hour_unit == "kWh"
        assert period.relative_price in relative_prices
```
## Developer Resources

[API Documentation](https://www.energidataservice.dk/tso-electricity/elspotprices#metadata-info)

[![Code%20Quality Pass](https://img.shields.io/badge/Code%20Quality-Pass-success?style=for-the-badge)](report/lint/index.html)
[![Tests Pass](https://img.shields.io/badge/Tests-Pass-success?style=for-the-badge)](report/test/index.html)