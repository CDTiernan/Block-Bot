# -*- coding: utf-8 -*-
# Python3.4*

from Bot.Strategies.CTStrategy import CTStrategy
from Bot.Strategies.CTStrategyTwoBlock import CTStrategyTwoBlock



def create(strategyType, game, params):
    switcher = {
        "ct": CTStrategy(game),
        "ct2b": CTStrategyTwoBlock(game,params)
    }

    strategy = switcher.get(strategyType.lower())

    return Planner(strategy)


class Planner:
    def __init__(self, strategy):
        self._strategy = strategy

    def makeMove(self):
        return self._strategy.choose()
