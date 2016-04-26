# -*- coding: utf-8 -*-
# Python3.4*

from Bot.Strategies.CTStrategyQuickMoves import CTStrategyQuickMoves



def create(strategyType, game, params):
    switcher = {
        "ctstratquick": CTStrategyQuickMoves(game,params)
    }

    strategy = switcher.get(strategyType.lower())

    return Planner(strategy)


class Planner:
    def __init__(self, strategy):
        self._strategy = strategy

    def makeMove(self):
        return self._strategy.choose()
