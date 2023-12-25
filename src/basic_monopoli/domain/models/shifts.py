from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from basic_monopoli.domain.ports.users import UserPort


@dataclass
class Shift:
    die_value: int
    user: "UserPort"
