from .domain.utils.inputs import get_yes_no_inpout, get_int_input
from .domain.ports.users import UserPort
from .adapters.scoreboard import ScoreBoard
from .domain.models import Building, Shift
from .domain.utils.boxes import get_properties_value
from .adapters.users import HumanUser, PcUser

scoreboard = ScoreBoard()


def users_setup():
    users_number = get_int_input(label="How many users?")
    users: list[UserPort] = []
    for index in range(users_number):
        print(f"User #{index}")
        is_pc_str = get_yes_no_inpout("Is Pc?")
        if is_pc_str:
            user = PcUser(
                money=1500,
                scoreboard=scoreboard,
                position=scoreboard.boxes[0],
            )
        else:
            user_name = input("Name:") or None
            user = HumanUser(
                money=1500,
                _name=user_name,
                scoreboard=scoreboard,
                position=scoreboard.boxes[0],
            )
        users.append(user)
    print("Shifts")
    shifts: list[Shift] = []
    for user in users:
        print(f"User {user.name} throws the die")
        die_value = scoreboard.throw_die()
        print(f"Result: {die_value}")
        shifts.append(Shift(die_value=die_value, user=user))
    shifts = sorted(shifts, key=lambda shift: shift.die_value)
    return list(map(lambda shift: shift.user, shifts))


def main():
    print("Start Monopoli")
    users = users_setup()
    round_number = 1
    game_condition = True
    ranking: list[tuple[UserPort, int | None]] = []
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
                    result = user.get_user_wants_to_buy(
                        label=f"Do you want to buy {new_position.name}?"
                    )
                    if result:
                        user.buy_property(box=new_position)
            else:
                if new_position.owner == user:
                    if new_position.hotels == 0:
                        try:
                            user.get_user_wants_to_buy_building(
                                position=new_position, building=Building.HOUSE
                            )
                        except new_position.MaximumHouseNumberReachedException:
                            user.get_user_wants_to_buy_building(
                                position=new_position, building=Building.HOTEL
                            )
                            continue
                    if new_position.houses == 4 or new_position.hotels > 0:
                        try:
                            user.get_user_wants_to_buy_building(
                                position=new_position, building=Building.HOTEL
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
                                user.sell_selected_properties(
                                    properties=user_properties
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
