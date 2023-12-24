import random, time

from enum import Enum
from functools import cached_property
from dataclasses import dataclass
from typing import ClassVar, Optional, Any
from functools import reduce


class Building(Enum):
    HOUSE = 0
    HOTEL = 1


@dataclass
class Box:
    name: str
    box_type: "BoxType"
    index: int
    houses: int = 0
    hotels: int = 0
    owner: Optional["User"] = None
    _base_rent: float | None = None
    _base_price: float | None = None
    _house_price: float | None = None
    _hotel_price: float | None = None

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

    class BoxType(Enum):
        CHEAP = 1
        MEDIUM = 2
        EXPENSIVE = 3

    class MaximumHouseNumberReachedException(Exception):
        pass

    class MaximumHotelNumberReachedException(Exception):
        pass

    @cached_property
    def base_rent(self):
        if self._base_rent:
            return self._base_rent
        return self.box_type.value * 75

    @cached_property
    def base_price(self):
        if self._base_price:
            return self._base_price
        return self.box_type.value * 150

    @cached_property
    def house_price(self):
        if self._house_price:
            return self._house_price
        return self.box_type.value * 35

    @cached_property
    def hotel_price(self):
        if self._hotel_price:
            return self._hotel_price
        return self.box_type.value * 85

    def get_rent(self):
        rent = self.base_rent
        rent += self.houses * (self.house_price / 4)
        rent += self.hotels * (self.hotel_price / 4)
        return rent

    def get_price(self):
        price = self.base_price
        price += self.houses * (self.house_price * 1.2)
        price += self.hotels * (self.house_price * 1.5)
        return price

    def user_can_buy(self, user: "User"):
        if self.owner is None:
            price = self.get_price()
            return price <= user.money
        return False

    def can_buy_house(self):
        return self.houses < 4

    def can_buy_hotel(self):
        return self.hotels < 4

    def add_hotel(self):
        self.houses = 0
        if not self.can_buy_hotel():
            raise self.MaximumHotelNumberReachedException()
        self.hotels += 1

    def add_house(self):
        if not self.can_buy_house():
            raise self.MaximumHouseNumberReachedException()
        self.houses += 1


class ScoreBoard:
    def __init__(self):
        self.boxes = list(self.get_boxes())
        self.n_boxes = len(self.boxes)

    def get_boxes(self):
        letters = ["a", "b", "c", "d"]
        indexes = list(range(1, 9))
        scoreboard_index = 0
        box_types = list(Box.BoxType)
        for letter in letters:
            for index in indexes:
                box_name = f"{letter}-{index}"
                scoreboard_index += 1
                yield Box(
                    name=box_name,
                    index=scoreboard_index,
                    box_type=random.choice(box_types),
                )

    def loop_completed(self, user: "User"):
        loop_reward = 100
        user.recieve_money(money=loop_reward, silently=True)
        print(
            f"User {user.name} completed a loop, € {loop_reward} added to your account"
        )

    def throw_die(self):
        return random.randint(1, 6)

    def throw_dice(self):
        print("Throwing dice...")
        return self.throw_die(), self.throw_die()

    def get_movement(self):
        die1, die2 = self.throw_dice()
        movement = die1 + die2
        print(f"{die1} + {die2} = {movement}")
        return movement

    def get_new_index(self, user: "User", initial_position: Box):
        movement = self.get_movement()
        new_index = initial_position.index + movement
        if new_index > self.n_boxes:
            self.loop_completed(user=user)
            new_index = new_index - self.n_boxes
        return new_index

    def get_new_position(self, new_index: int):
        return next(filter(lambda box: box.index == new_index, self.boxes))


scoreboard = ScoreBoard()


@dataclass
class User:
    money: float
    position: Box
    is_pc: bool = False
    _name: str | None = None

    users: ClassVar[int] = 0

    def __post_init__(self):
        User.users += 1
        self.user_number = User.users

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
        if not isinstance(other, User):
            return False
        return self.name == other.name and self.user_number == other.user_number

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

    @cached_property
    def name(self):
        if self._name:
            return self._name
        return self.generate_name()

    def generate_name(self):
        if self.is_pc:
            return f"PC {self.user_number}"
        return f"User #{self.user_number}"

    def get_properties(self):
        return list(filter(lambda box: box.owner == self, scoreboard.boxes))

    def recieve_money(
        self,
        money: float,
        giver: Optional["User"] = None,
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
        reciever: Optional["User"] = None,
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

    def pay_rent(self, box: Box):
        if not box.owner:
            raise self.PropertyNotOwnedException()
        if box.owner == self:
            raise self.NoRentNeededException()
        rent = box.get_rent()
        try:
            self.give_money(money=rent, reciever=box.owner)
        except self.CantAffordException:
            raise self.CantAffordRentException()
        else:
            print(f"{self.name} paid rent for {box.name} to {box.owner.name}")

    def buy_property(self, box: Box):
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

    def sell_property(self, box: Box):
        if box.owner != self:
            raise self.PropertyNotOwnedException()
        box_value = box.get_price()
        box.houses = 0
        box.hotels = 0
        box.owner = None
        self.recieve_money(money=box_value, silently=True)
        return box_value

    def buy_building(self, box: Box, building: Building):
        if box.owner != self:
            raise self.PropertyNotOwnedException()
        if building == Building.HOUSE:
            price = box.house_price
            Exc = self.CantAffordHouseException
            callback = box.add_house
        else:
            price = box.hotel_price
            Exc = self.CantAffordHotelException
            callback = box.add_hotel
        try:
            self.give_money(money=price)
        except self.CantAffordException:
            raise Exc()
        else:
            callback()

    def bankrupt(self):
        for _ in range(3):
            print("WARNING")
            time.sleep(0.5)
        print("BANKRUPT")
        print(f"User {self.name} went bankrupt")


YES = "Y"
NO = "N"


def get_yes_no_inpout(label: str):
    result = input(label + f' ("{YES}"/"{NO}")')
    if result.upper() in [YES, NO]:
        return result.upper()
    else:
        print("Enter a correct answer")
        return get_yes_no_inpout(label=label)


def users_setup():
    users_number = 0

    while users_number == 0:
        try:
            users_number = int(input("How many users?"))
        except ValueError:
            print("Enter a correct number")
            users_number = 0
        else:
            pass

    users: list[User] = []
    for index in range(users_number):
        print(f"User #{index}")
        is_pc_str = get_yes_no_inpout("Is Pc?")
        if is_pc_str == YES:
            user = User(money=1500, is_pc=True, position=scoreboard.boxes[0])
        else:
            user_name = input("Name:") or None
            user = User(
                money=1500, _name=user_name, position=scoreboard.boxes[0]
            )
        users.append(user)

    @dataclass
    class Shift:
        die_value: int
        user: User

    print("Shifts")
    shifts: list[Shift] = []
    for user in users:
        print(f"User {user.name} throws the die")
        die_value = scoreboard.throw_die()
        print(f"Result: {die_value}")
        shifts.append(Shift(die_value=die_value, user=user))
    shifts = sorted(shifts, key=lambda shift: shift.die_value)
    return list(map(lambda shift: shift.user, shifts))


def get_user_can_buy_box(user: User):
    return user.position.owner != user


def display_properties(properties: list[Box]):
    for index, box in enumerate(properties, start=1):
        print(f"{index} | {box}")


def select_properties(
    properties: list[Box], message: str = "Select properties (1,2,3,...): "
):
    display_properties(properties=properties)
    result_str = input(message)
    result = result_str.split(",")
    try:
        selected_index = list(map(int, result))
    except ValueError:
        print("Add a correct list of indexes")
        return select_properties(properties=properties)
    else:
        try:
            selected_properties = list(
                map(lambda index: properties[index], selected_index)
            )
        except IndexError:
            print("Add a correct list of indexes")
            return select_properties(properties=properties)
        else:
            return selected_properties


def get_properties_value(properties: list[Box]):
    prices = map(lambda box: box.get_price(), properties)
    value = reduce(lambda tot, price: tot + price, prices, 0.0)
    return value


def select_properties_to_sell(user: User, properties: list[Box]):
    if user.is_pc:
        selled_properties = [properties[0]]
    else:
        selled_properties = select_properties(
            properties=properties,
            message="Select properties to sell (1,2,3,...): ",
        )
    print("You are about to sell: ")
    display_properties(properties=selled_properties)
    profit = get_properties_value(selled_properties)
    print(f"To earn € {profit}")
    if user.is_pc:
        result = YES
    else:
        result = get_yes_no_inpout("Are you sure?")
    if result == NO:
        return select_properties_to_sell(user=user, properties=properties)
    else:
        for box in selled_properties:
            box_profit = user.sell_property(box=box)
            print(f"Selled {box.name} for € {box_profit}")


def ask_user_to_buy_building(user: User, position: Box, building: Building):
    if building == Building.HOUSE:
        number = position.houses
        price = position.house_price
        name = "house"
    else:
        number = position.hotels
        price = position.hotel_price
        name = "hotel"
    if position.houses < 4:
        while number < 4 and user.money > price:
            if user.is_pc:
                result = YES
            else:
                result = get_yes_no_inpout(
                    f"Do you want to buy a new {name}? Now {number}"
                )
            if result == YES:
                user.buy_building(box=position, building=building)
            else:
                break


def main():
    print("Start Monopoli")
    users = users_setup()
    round_number = 1
    game_condition = True
    ranking: list[tuple[User, int | None]] = []
    while game_condition:
        print(f"Start Round {round_number}")
        for user in users:
            print(f"User: {user.name}")
            print(str(user))
            new_index = scoreboard.get_new_index(
                user=user, initial_position=user.position
            )
            new_position = scoreboard.get_new_position(new_index=new_index)
            print("New Position!")
            print(str(new_position))
            user.position = new_position
            if new_position.owner is None:
                if new_position.user_can_buy(user=user):
                    if not user.is_pc:
                        result = get_yes_no_inpout(
                            f"Do you want to buy {new_position.name}?"
                        )
                        if result == YES:
                            user.buy_property(box=new_position)
                    else:
                        user.buy_property(box=new_position)
            else:
                if new_position.owner == user:
                    if new_position.hotels == 0:
                        try:
                            ask_user_to_buy_building(
                                user=user,
                                position=new_position,
                                building=Building.HOUSE,
                            )
                        except new_position.MaximumHouseNumberReachedException:
                            ask_user_to_buy_building(
                                user=user,
                                position=new_position,
                                building=Building.HOTEL,
                            )
                            continue
                    if new_position.houses == 4 or new_position.hotels > 0:
                        try:
                            ask_user_to_buy_building(
                                user=user,
                                position=new_position,
                                building=Building.HOTEL,
                            )
                        except new_position.MaximumHotelNumberReachedException:
                            continue
                else:
                    print("You have to pay the rent")
                    try:
                        user.pay_rent(box=new_position)
                    except user.CantAffordRentException:
                        print("Ops! You don't have enough money!")
                        user_properties = user.get_properties()
                        user_properties_values = get_properties_value(
                            properties=user_properties
                        )
                        rent = new_position.get_rent()
                        if (
                            len(user_properties)
                            and user_properties_values > rent
                        ):
                            while user.money < rent:
                                select_properties_to_sell(
                                    user=user, properties=user_properties
                                )
                                user_properties = user.get_properties()
                            user.pay_rent(box=new_position)
                        else:
                            user.bankrupt()
                            user.give_money(
                                money=user.money,
                                reciever=new_position.owner,
                                silently=True,
                            )
                            print(
                                f"User {user.name} gived all the money to {new_position.owner.name}"
                            )
                            users.remove(user)
                            n_users = len(users)
                            ranking.append((user, round_number))
                            if n_users > 1:
                                print(f"{len(users)} users left")
                                continue
                            else:
                                ranking.append((users[0], None))
                                game_condition = False
                                break

                        print("Choose the property")
        round_number += 1
    ranking.reverse()
    print("Ranking:")
    for index, (user, rounds) in enumerate(ranking, start=1):
        rounds_label = str(rounds) if rounds else "WINNER"
        print(f"{index}: {user.name} {rounds_label}")


if __name__ == "__main__":
    main()
