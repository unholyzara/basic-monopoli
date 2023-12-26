from basic_monopoli.domain.models.shifts import Shift
from basic_monopoli.domain.ports.scoreboards import ScoreBoardPort
from basic_monopoli.domain.ports.users import UserPort
from basic_monopoli.domain.ports.users_setuppers import UsersSetupperPort
from basic_monopoli.domain.utils.inputs import get_int_input, get_yes_no_inpout
from .users import HumanUser, PcUser


class UsersSetupper(UsersSetupperPort):
    def create_users(self, scoreboard: ScoreBoardPort) -> list[UserPort]:
        users_number = get_int_input(label="How many users?")
        users: list[UserPort] = []
        initial_postion = scoreboard.get_initial_position()
        for index in range(users_number):
            print(f"User #{index}")
            is_pc_str = get_yes_no_inpout("Is Pc?")
            if is_pc_str:
                user = PcUser(money=1500, position=initial_postion)
            else:
                user_name = input("Name (optional):") or None
                user = HumanUser(
                    money=1500, _name=user_name, position=initial_postion
                )
            users.append(user)
        return users

    def get_shifts(self, users: list[UserPort], scoreboard: ScoreBoardPort):
        shifts: list[Shift] = []
        for user in users:
            print(f"User {user.name} throws the die")
            die_value = scoreboard.throw_die()
            print(f"Result: {die_value}")
            shifts.append(Shift(die_value=die_value, user=user))
        return shifts
