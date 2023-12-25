from typing import Sequence

from ..ports.boxes import BaseBoxPort


def display_properties(properties: Sequence["BaseBoxPort"]):
    for index, box in enumerate(properties, start=1):
        print(f"{index} | {box}")
