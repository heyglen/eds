import datetime


class RelativeCost:
    expensive = 1
    mid_priced = 2
    cheap = 3
    unknown = 4


class Period:
    def __init__(
        self,
        when: datetime.datetime,
        price: float,
        currency="dkk",
        currency_unit="øre",
        hour_unit="kWh",
        relative_price=RelativeCost.unknown,
    ):
        self.when = when
        self.price = price
        self.currency = currency
        self.currency_unit = currency_unit
        self.hour_unit = hour_unit
        self.relative_price = relative_price

    def __str__(self):
        when = self.when.strftime("%Y.%m.%d %H:%M")
        return f"{when} {self.price:3} {self.currency_unit}"
