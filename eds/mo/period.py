import datetime
import enum
from dataclasses import dataclass

import click


class RelativeCost(enum.Enum):
    expensive = enum.auto()
    normal = enum.auto()
    cheap = enum.auto()
    unknown = enum.auto()


@dataclass
class Period:
    when: datetime.datetime
    price: float
    currency = "dkk"
    currency_unit = "øre"
    hour_unit = "kWh"
    relative_price = RelativeCost.unknown

    def __str__(self):
        when = self.when.strftime("%Y.%m.%d %H:%M")
        return f"{when} {self.price:3} {self.currency_unit}"

    def click_format(self, time_only=False) -> str:
        if time_only:
            when = self.when.strftime("%H:%M")
        else:
            when = self.when.strftime("%Y.%m.%d %H:%M")
        cost = f"{self.price:3}"
        if self.relative_price == RelativeCost.cheap:
            cost = click.style(f"{self.price:3}", fg="green")
        elif self.relative_price == RelativeCost.expensive:
            cost = click.style(f"{self.price:3}", fg="red")
        return f"{when} {cost} {self.currency_unit}"
