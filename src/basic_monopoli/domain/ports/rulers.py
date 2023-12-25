import abc


class RulerPort(abc.ABC):
    @abc.abstractmethod
    def get_initial_money(self) -> int | float:
        pass

    @abc.abstractmethod
    def get_loop_reward(self) -> float:
        pass

    @abc.abstractmethod
    def get_max_houses(self) -> int:
        pass

    @abc.abstractmethod
    def get_max_hotels(self) -> int:
        pass

    def get_group_owned_multiplier(self) -> int | float:
        return 2
