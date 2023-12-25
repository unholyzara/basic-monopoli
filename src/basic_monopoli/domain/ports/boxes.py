import abc

from dataclasses import dataclass
from typing import Optional

from .users import UserPort
from .rulers import RulerPort
from .scoreboards import ScoreBoardPort


@dataclass(kw_only=True)
class BaseBoxPort(abc.ABC):
    name: str
    index: int
    scoreboard: ScoreBoardPort
    ruler: RulerPort
    group = None
    owner = None

    def __str__(self):
        return self.name

    @abc.abstractmethod
    def step_on(self, user: UserPort, ruler: RulerPort):
        pass

    def movement_step_on(self, user: UserPort, ruler: RulerPort):
        pass

    def user_can_buy(self, user: UserPort):
        return False


@dataclass
class RentOnlyBoxPort(BaseBoxPort):
    @abc.abstractmethod
    def get_rent(self) -> float:
        pass


@dataclass
class PropertyBoxPort(RentOnlyBoxPort):
    owner: Optional[UserPort] = None
    houses: int = 0
    hotels: int = 0

    class MaximumHouseNumberReachedException(Exception):
        pass

    class MaximumHotelNumberReachedException(Exception):
        pass

    def __str__(self):
        owner = self.owner.name if self.owner else "Free"
        label_ls = [
            f"Name: {self.name}",
            f"Owner: {owner}",
            f"Price: {self.get_price()}",
            f"Rent: {self.get_rent()}",
            f"Houses: {self.houses}",
            f"Hotels: {self.hotels}",
        ]
        return " | ".join(label_ls)

    @abc.abstractmethod
    def get_price(self) -> float:
        pass

    def user_can_buy(self, user: UserPort):
        if self.owner is None:
            price = self.get_price()
            return price <= user.money
        return False

    def handle_purchasable_property(self, user: UserPort):
        if self.user_can_buy(user=user):
            result = user.get_user_wants_to_buy(
                label=f"Do you want to buy {self.name}?"
            )
            if result:
                user.buy_property(box=self)

    def handle_owned_property(self):
        # TODO: Houses & Hotels
        pass

    def step_on(self, user: UserPort, ruler: RulerPort):
        user.position = self
        if self.owner is None:
            self.handle_purchasable_property(user=user)
        else:
            if self.owner == user:
                self.handle_owned_property()
            else:
                user.pay_rent(box=self)


BoxPortType = BaseBoxPort | RentOnlyBoxPort | PropertyBoxPort
