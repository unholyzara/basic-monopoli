from basic_monopoli.domain.models.shifts import Shift
from basic_monopoli.domain.ports.users import UserPort
from basic_monopoli.domain.ports.users_setuppers import UsersSetupperPort
from basic_monopoli.domain.utils.inputs import get_int_input, get_yes_no_inpout
from .users import HumanUser, PcUser


class UsersSetupper(UsersSetupperPort):
    def get_users(self):
        users_number = get_int_input(label="How many users?")
        users: list[UserPort] = []
        for index in range(users_number):
            print(f"User #{index}")
            is_pc_str = get_yes_no_inpout("Is Pc?")
            if is_pc_str:
                user = PcUser(
                    money=1500,
                    scoreboard=self.scoreboard,
                    position=self.scoreboard.get_initial_position(),
                )
            else:
                user_name = input("Name (optional):") or None
                user = HumanUser(
                    money=1500,
                    _name=user_name,
                    scoreboard=self.scoreboard,
                    position=self.scoreboard.get_initial_position(),
                )
            users.append(user)
        return users

    def get_shifts(self, users: list[UserPort]):
        print("Shifts")
        shifts: list[Shift] = []
        for user in users:
            print(f"User {user.name} throws the die")
            die_value = self.scoreboard.throw_die()
            print(f"Result: {die_value}")
            shifts.append(Shift(die_value=die_value, user=user))
        return shifts
