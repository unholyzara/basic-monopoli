from dataclasses import dataclass
from copy import deepcopy

from .ports.users import UserPort
from .ports.scoreboards import ScoreBoardPort
from .ports.users_setuppers import UsersSetupperPort
from .ports.rulers import RulerPort
from .ports.boxes import BoxPortType, BaseBoxPort, RentOnlyBoxPort
from .utils.boxes import get_properties_value
from .actions import Actions


@dataclass
class Monopoly:
    setupper: UsersSetupperPort
    scoreboard: ScoreBoardPort
    ruler: RulerPort

    def __post_init__(self):
        self.round_number = 1
        self.game_toggle = False
        self.ranking: list[tuple[UserPort, int | None]] = []
        self.in_game_users = deepcopy(self.setupper.users)

    @property
    def game_condition(self):
        return self.game_toggle and len(self.in_game_users) > 1

    def initialize(self):
        self.game_toggle = True

    def start_round(self):
        print(f"Start Round {self.round_number}")

    def start_user_round(self, user: UserPort):
        print(f"User: {user.name}")
        print(str(user))

    def remove_user(self, user: UserPort):
        self.in_game_users.remove(user)
        n_users = len(self.in_game_users)
        self.ranking.append((user, self.round_number))
        if n_users > 1:
            print(f"{len(self.in_game_users)} users left")
        else:
            self.ranking.append((self.in_game_users[0], None))

    def user_game_over(self, user: UserPort, position: "BaseBoxPort"):
        user.bankrupt()
        owner = position.owner
        if owner is not None:
            user.give_money(money=user.money, reciever=owner, silently=True)
            print(f"User {user.name} gived all the money to {owner.get_name()}")
        self.remove_user(user=user)

    def handle_user_cant_afford_rent(
        self, position: RentOnlyBoxPort, user: UserPort
    ):
        print("Ops! You don't have enough money!")
        user_properties = user.get_properties()
        user_properties_values = get_properties_value(
            properties=user_properties
        )
        rent = position.get_rent()
        if len(user_properties) and user_properties_values > rent:
            while user.money < rent:
                user.sell_selected_properties(properties=user_properties)
                user_properties = user.get_properties()
            user.pay_rent(box=position)
        else:
            self.user_game_over(user=user, position=position)

    def step_on_box(self, user: UserPort, position: BoxPortType):
        if isinstance(position, RentOnlyBoxPort):
            try:
                position.step_on(user=user)
            except user.CantAffordRentException:
                self.handle_user_cant_afford_rent(position=position, user=user)
        else:
            position.step_on(user=user)

    def user_round(self, user: UserPort):
        self.start_user_round(user=user)
        Actions.choose_action(user=user)
        new_index = self.scoreboard.get_new_index(
            user=user, initial_position=user.position
        )
        new_position = self.scoreboard.get_new_position(new_index=new_index)
        print("New Position!")
        print(str(new_position))
        self.step_on_box(user=user, position=new_position)

    def round(self):
        for user in self.in_game_users:
            self.user_round(user=user)

    def end_round(self):
        self.round_number += 1

    def play(self):
        while self.game_condition:
            self.start_round()
            self.end_round()

    def end(self):
        ranking = deepcopy(self.ranking)
        ranking.reverse()
        print("Ranking:")
        for index, (user, rounds) in enumerate(ranking, start=1):
            rounds_label = str(rounds) if rounds else "WINNER"
            print(f"{index}: {user.name} {rounds_label}")
        print("Thanks for playing")


def game(
    setupper: UsersSetupperPort, scoreboard: ScoreBoardPort, ruler: RulerPort
):
    game = Monopoly(setupper=setupper, scoreboard=scoreboard, ruler=ruler)
    game.play()
    game.end()
