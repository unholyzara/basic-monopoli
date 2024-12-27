from enum import Enum
from dataclasses import dataclass

from basic_monopoli.domain.models.groups import PropertyBoxGroup
from basic_monopoli.domain.ports.users import UserPort
from basic_monopoli.domain.ports.boxes import BaseBoxPort, PropertyBoxPort


@dataclass
class StartingBox(BaseBoxPort):
    def step_on(self, user: UserPort):
        self.movement_step_on(user=user)

    def movement_step_on(self, user: UserPort):
        loop_reward = self.ruler.get_loop_reward()
        user.recieve_money(money=loop_reward, silently=True)
        print("You completed a loop")
        print(f"€ {loop_reward} added to your account")


@dataclass
class StepOnlyBox(BaseBoxPort):
    def step_on(self, user: UserPort):
        pass


@dataclass
class ChanceBox(BaseBoxPort):
    name: str = "Imprevisiti"

    def step_on(self, user: UserPort):
        pass


@dataclass
class ProbabilityBox(BaseBoxPort):
    name: str = "Probabilità"

    def step_on(self, user: UserPort):
        pass


@dataclass
class PrisonBox(BaseBoxPort):
    name: str = "Prigione"

    def step_on(self, user: UserPort):
        pass


@dataclass(kw_only=True)
class BasicPropertyBox(PropertyBoxPort):
    box_type: "BoxType"

    class BoxType(Enum):
        CHEAP = 1
        MEDIUM = 2
        EXPENSIVE = 3

    def get_base_rent(self) -> float:
        return self.box_type.value * 75

    def get_house_price(self) -> float:
        return self.box_type.value * 35

    def get_hotel_price(self) -> float:
        return self.box_type.value * 85

    def get_rent(self):
        rent = self.get_base_rent()
        rent += self.level * (rent / 4)
        return rent

    def get_price(self):
        return self.box_type.value * 150


@dataclass(kw_only=True)
class PropertyBox(PropertyBoxPort):
    group: PropertyBoxGroup
    base_rent: float
    base_price: float
    house_price: float
    hotel_price: float

    @property
    def same_group_owned(self):
        same_owner_group_boxes = list(
            filter(lambda box: box.owner == self.owner, self.scoreboard.boxes)
        )
        return same_owner_group_boxes

    @property
    def group_is_owned(self):
        same_group_boxes = list(
            filter(lambda box: box.group == self.group, self.scoreboard.boxes)
        )
        if not same_group_boxes:
            return False
        return len(self.same_group_owned) == len(same_group_boxes)

    def get_price(self) -> float:
        return self.base_price

    def get_rent(self) -> float:
        rent = self.base_rent
        if self.owner is not None:
            if self.group_is_owned:
                rent *= self.ruler.get_group_owned_multiplier()
        return rent
