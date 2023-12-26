import abc

from .users import UserPort
from .scoreboards import ScoreBoardPort
from ..models.shifts import Shift


class UsersSetupperPort(abc.ABC):
    @abc.abstractmethod
    def create_users(self, scoreboard: ScoreBoardPort) -> list[UserPort]:
        pass

    @abc.abstractmethod
    def get_shifts(
        self, users: list[UserPort], scoreboard: ScoreBoardPort
    ) -> list[Shift]:
        pass

    def get_users(self, scoreboard: ScoreBoardPort):
        users = self.create_users(scoreboard=scoreboard)
        print("Shifts")
        shifts = self.get_shifts(users=users, scoreboard=scoreboard)
        return self.order_users(shifts=shifts)

    def order_users(self, shifts: list[Shift]):
        shifts = sorted(shifts, key=lambda shift: shift.die_value)
        return list(map(lambda shift: shift.user, shifts))
