from basic_monopoli.domain.ports.rulers import RulerPort
from basic_monopoli.domain.ports.scoreboards import ScoreBoardPort

from basic_monopoli.adapters.rulers import standard_ruler
from basic_monopoli.adapters.scoreboard import StandardScoreBoard
from basic_monopoli.adapters.users_setuppers import UsersSetupper

from basic_monopoli.domain.commands import game


def monopoly(
    ruler: RulerPort | None = None, scoreboard: ScoreBoardPort | None = None
):
    if ruler is None:
        ruler = standard_ruler
    if scoreboard is None:
        scoreboard = StandardScoreBoard(ruler=ruler)
    setupper = UsersSetupper(scoreboard=scoreboard)
    game(setupper=setupper, scoreboard=scoreboard, ruler=ruler)
