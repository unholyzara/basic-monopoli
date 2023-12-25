import abc

from dataclasses import dataclass

from .users import UserPort
from .scoreboards import ScoreBoardPort
from ..models.shifts import Shift


@dataclass
class UsersSetupperPort(abc.ABC):
    scoreboard: ScoreBoardPort

    def __post_init__(self):
        users = self.get_users()
        shifts = self.get_shifts(users=users)
        self.users = self.order_users(shifts=shifts)

    @abc.abstractmethod
    def get_users(self) -> list[UserPort]:
        pass

    @abc.abstractmethod
    def get_shifts(self, users: list[UserPort]) -> list[Shift]:
        pass

    def order_users(self, shifts: list[Shift]):
        shifts = sorted(shifts, key=lambda shift: shift.die_value)
        return list(map(lambda shift: shift.user, shifts))
