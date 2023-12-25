import random

from dataclasses import dataclass

from basic_monopoli.domain.ports.scoreboards import ScoreBoardPort
from basic_monopoli.domain.ports.rulers import RulerPort
from .boxes import BasicPropertyBox


@dataclass
class ScoreBoard(ScoreBoardPort):
    ruler: RulerPort

    def get_boxes(self):
        letters = ["a", "b", "c", "d"]
        indexes = list(range(1, 9))
        scoreboard_index = 0
        box_types = list(BasicPropertyBox.BoxType)
        for letter in letters:
            for index in indexes:
                box_name = f"{letter}-{index}"
                scoreboard_index += 1
                yield BasicPropertyBox(
                    name=box_name,
                    index=scoreboard_index,
                    box_type=random.choice(box_types),
                    scoreboard=self,
                    ruler=self.ruler,
                )
