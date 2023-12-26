from typing import Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from basic_monopoli.domain.ports.boxes import BaseBoxPort


def display_properties(properties: Sequence["BaseBoxPort"]):
    for index, box in enumerate(properties, start=1):
        print(f"{index} | {box}")


def display_money(money: int | float):
    return f"€ {money:.2f}"
