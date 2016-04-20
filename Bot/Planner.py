# -*- coding: utf-8 -*-
# Python3.4*

from Bot.Strategies.RandomStrategy import RandomStrategy
from Bot.Strategies.CTStrategy import CTStrategy
from Bot.Strategies.CTStrategyTwoBlock import CTStrategyTwoBlock
from Bot.Strategies.CTStrategySmartTwoBlock import CTStrategySmartTwoBlock



def create(strategyType, game, params):
    switcher = {
        "random": RandomStrategy(game),
        "ctstrat": CTStrategy(game),
        "ctstrat2block": CTStrategyTwoBlock(game),
        "ctstratsmart2block": CTStrategySmartTwoBlock(game,params)
    }

    strategy = switcher.get(strategyType.lower())

    return Planner(strategy)


class Planner:
    def __init__(self, strategy):
        self._strategy = strategy

    def makeMove(self):
        return self._strategy.choose()
