import random, abc

from typing import Iterator
from dataclasses import dataclass

from .users import UserPort
from .boxes import BoxPortType


@dataclass
class ScoreBoardPort(abc.ABC):
    def __post_init__(self):
        self.boxes = list(self.get_boxes())
        self.n_boxes = len(self.boxes)

    @abc.abstractmethod
    def get_boxes(self) -> Iterator[BoxPortType]:
        pass

    def get_initial_position(self):
        return self.boxes[0]

    def loop_completed(self, user: UserPort):
        loop_reward = 100
        user.recieve_money(money=loop_reward, silently=True)
        print(
            f"AbstractUser {user.name} completed a loop, € {loop_reward} added to your account"
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

    def get_new_index(self, user: UserPort, initial_position: BoxPortType):
        movement = self.get_movement()
        new_index = initial_position.index + movement
        if new_index > self.n_boxes:
            self.loop_completed(user=user)
            new_index = new_index - self.n_boxes
        else:
            return new_index

    def get_new_position(self, new_index: int):
        return next(filter(lambda box: box.index == new_index, self.boxes))
