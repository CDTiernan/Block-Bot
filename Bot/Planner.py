# -*- coding: utf-8 -*-
# Python3.4*

from Bot.Strategies.RandomStrategy import RandomStrategy
from Bot.Strategies.CTStrategy import CTStrategy


def create(strategyType, game):
    switcher = {
        "random": RandomStrategy(game),
        "ctstrat": CTStrategy(game)
    }

    strategy = switcher.get(strategyType.lower())

    return Planner(strategy)


class Planner:
    def __init__(self, strategy):
        self._strategy = strategy

    def makeMove(self):
        return self._strategy.choose()
