from dataclasses import dataclass

from basic_monopoli.domain.ports.rulers import RulerPort


@dataclass
class Ruler(RulerPort):
    initial_money: int | float
    loop_reward: int | float
    max_houses: int
    max_hotels: int

    def get_initial_money(self) -> int | float:
        return self.initial_money

    def get_loop_reward(self) -> float:
        return self.loop_reward

    def get_max_houses(self) -> int:
        return self.max_houses

    def get_max_hotels(self) -> int:
        return self.max_hotels


standard_ruler = Ruler(
    initial_money=1500, loop_reward=200, max_houses=4, max_hotels=4
)
