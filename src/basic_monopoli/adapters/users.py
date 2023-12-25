import abc

from functools import cached_property
from dataclasses import dataclass
from typing import ClassVar, Any

from basic_monopoli.domain.utils.inputs import get_yes_no_inpout
from basic_monopoli.domain.models.buildings import Building
from basic_monopoli.domain.utils.inputs import select_properties
from basic_monopoli.domain.ports.users import UserPort
from basic_monopoli.domain.ports.boxes import BoxPortType, PropertyBoxPort
from basic_monopoli.domain.ports.scoreboards import ScoreBoardPort


@dataclass
class BaseUser(UserPort):
    scoreboard: ScoreBoardPort
    money: float
    position: BoxPortType

    users: ClassVar[int] = 0

    def __post_init__(self):
        HumanUser.users += 1
        self.user_number = HumanUser.users

    def __str__(self):
        properties = self.get_properties()
        label_ls = [
            f"Name: {self.name}",
            f"Money: {self.money}",
            f"Properties: {len(properties)}",
        ]
        label = " | ".join(label_ls)
        properties_str_ls: list[str] = []
        for index, box in enumerate(properties, start=1):
            properties_str_ls.append(f"{index} | {box}")
        properties_str = "\n".join(properties_str_ls)
        return label + properties_str

    def __eq__(self, other: Any):
        if not isinstance(other, BaseUser):
            return False
        return self.name == other.name and self.user_number == other.user_number

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @cached_property
    def name(self):
        return self.get_name()


@dataclass
class HumanUser(BaseUser):
    _name: str | None = None

    def generate_name(self):
        return f"User #{self.user_number}"

    def get_name(self):
        if self._name:
            return self._name
        return self.generate_name()

    def get_user_wants_to_buy(self, label: str):
        return get_yes_no_inpout(label=label)

    def get_user_wants_to_buy_building(
        self, position: PropertyBoxPort, building: Building
    ):
        if building == Building.HOUSE:
            number = position.houses
            name = "house"
        else:
            number = position.hotels
            name = "hotel"
        return get_yes_no_inpout(
            label=f"Do you want to buy a new {name}? Now {number}"
        )

    def get_if_user_is_sure(self, label: str):
        return get_yes_no_inpout(label=label)

    def get_which_properties_to_sell(self, properties: list[PropertyBoxPort]):
        return select_properties(
            properties=properties,
            message="Select properties to sell (1,2,3,...): ",
        )


class PcUser(BaseUser):
    def get_name(self):
        return f"PC {self.user_number}"

    def get_user_wants_to_buy(self, label: str):
        return True

    def get_user_wants_to_buy_building(
        self, position: PropertyBoxPort, building: Building
    ):
        return True

    def get_if_user_is_sure(self, label: str):
        return True

    def get_which_properties_to_sell(self, properties: list[PropertyBoxPort]):
        return [properties[0]]
