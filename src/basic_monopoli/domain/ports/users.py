import time, abc

from typing import Optional, Any, TYPE_CHECKING

from ..actions import Actions
from ..models.buildings import Building
from ..utils.boxes import get_properties_value
from ..utils.displays import display_properties
from .boxes import PropertyBoxPort, BoxPortType

if TYPE_CHECKING:
    from .scoreboards import ScoreBoardPort


class UserPort(abc.ABC):
    scoreboard: "ScoreBoardPort"
    money: float
    position: BoxPortType
    loop: int = 0

    class CantAffordException(Exception):
        pass

    class AlreadyBoughtException(Exception):
        pass

    class AlreadyOwnedPropertyException(Exception):
        pass

    class CantAffordPropertyException(CantAffordException):
        pass

    class PropertyNotOwnedException(Exception):
        pass

    class NoRentNeededException(Exception):
        pass

    class CantAffordRentException(CantAffordException):
        pass

    class CantAffordHouseException(CantAffordException):
        pass

    class CantAffordHotelException(CantAffordException):
        pass

    def __eq__(self, other: Any):
        return type(self) is type(other)

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def get_user_wants_to_buy(self, label: str) -> bool:
        pass

    @abc.abstractmethod
    def get_user_wants_to_buy_building(
        self, position: PropertyBoxPort, building: Building
    ) -> bool:
        pass

    @abc.abstractmethod
    def get_if_user_is_sure(self, label: str) -> bool:
        pass

    @abc.abstractmethod
    def get_which_properties_to_sell(
        self, properties: list[PropertyBoxPort]
    ) -> list[PropertyBoxPort]:
        pass

    @abc.abstractmethod
    def ask_user_what_to_do(self) -> Actions:
        pass

    def get_properties(
        self, scoreboard: "ScoreBoardPort"
    ) -> list[PropertyBoxPort]:
        return list(
            filter(lambda box: box.owner == self, scoreboard.boxes)  # type: ignore
        )

    def recieve_money(
        self,
        money: float,
        giver: Optional["UserPort"] = None,
        silently: bool = False,
    ):
        self.money += money
        message = f"{self.name} recieved € {money}"
        if giver is not None:
            message += f" from {giver.name}"
        if not silently:
            print(message)

    def give_money(
        self,
        money: float,
        reciever: Optional["UserPort"] = None,
        silently: bool = False,
    ):
        if money > self.money:
            raise self.CantAffordException()
        self.money -= money
        message = f"{self.name} paid € {money}"
        if reciever is not None:
            reciever.recieve_money(money=money)
            message += f" to {reciever.name}"
        if not silently:
            print(message)

    def pay_rent(self, box: PropertyBoxPort):
        if isinstance(box, PropertyBoxPort) and not box.owner:
            raise self.PropertyNotOwnedException()
        if box.owner == self:
            raise self.NoRentNeededException()
        rent = box.get_rent()
        try:
            self.give_money(money=rent, reciever=box.owner)
        except self.CantAffordException:
            raise self.CantAffordRentException()
        else:
            if box.owner:
                owner_str = box.owner.name
            else:
                owner_str = "the Bank"
            print(f"{self.name} paid rent for {box.name} to {owner_str}")

    def buy_property(self, box: PropertyBoxPort):
        if box.owner:
            if box.owner == self:
                raise self.AlreadyBoughtException()
            else:
                raise self.AlreadyOwnedPropertyException()
        box_price = box.get_price()
        try:
            self.give_money(money=box_price, reciever=box.owner)
        except self.CantAffordException:
            raise self.CantAffordPropertyException()
        else:
            box.owner = self
            print(f"{self.name} bought property {box.name}")

    def sell_property(self, box: PropertyBoxPort):
        if box.owner != self:
            raise self.PropertyNotOwnedException()
        box_value = box.get_price()
        box.houses = 0
        box.hotels = 0
        box.owner = None
        self.recieve_money(money=box_value, silently=True)
        return box_value

    def sell_selected_properties(self, properties: list[PropertyBoxPort]):
        selled_properties = self.get_which_properties_to_sell(
            properties=properties
        )
        print("You are about to sell: ")
        display_properties(properties=selled_properties)
        profit = get_properties_value(selled_properties)
        print(f"To earn € {profit}")
        result = self.get_if_user_is_sure(label="Are you sure?")
        if result:
            for box in selled_properties:
                box_profit = self.sell_property(box=box)
                print(f"Selled {box.name} for € {box_profit}")
        else:
            return self.sell_selected_properties(properties=properties)

    # def buy_building(self, box: "BasicBox", building: Building):
    #     if box.owner != self:
    #         raise self.PropertyNotOwnedException()
    #     if building == Building.HOUSE:
    #         price = box.house_price
    #         Exc = self.CantAffordHouseException
    #         callback = box.add_house
    #     else:
    #         price = box.hotel_price
    #         Exc = self.CantAffordHotelException
    #         callback = box.add_hotel
    #     try:
    #         self.give_money(money=price)
    #     except self.CantAffordException:
    #         raise Exc()
    #     else:
    #         callback()

    # def buy_several_buildings(self, position: "BasicBox", building: Building):
    #     if building == Building.HOUSE:
    #         number = position.houses
    #         price = position.house_price
    #     else:
    #         number = position.hotels
    #         price = position.hotel_price
    #     if position.houses < 4:
    #         while number < 4 and self.money > price:
    #             result = self.get_user_wants_to_buy_building(
    #                 position=position, building=building
    #             )
    #             if result:
    #                 self.buy_building(box=position, building=building)
    #             else:
    #                 break

    def bankrupt(self):
        for _ in range(3):
            print("WARNING")
            time.sleep(0.5)
        print("BANKRUPT")
        print(f"User {self.name} went bankrupt")
