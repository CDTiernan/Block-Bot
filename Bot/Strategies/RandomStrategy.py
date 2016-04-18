# -*- coding: utf-8 -*-
# Python3.4*

from random import randint
from Bot.Strategies.AbstractStrategy import AbstractStrategy


class RandomStrategy(AbstractStrategy):
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']

    def choose(self):
        ind = [randint(0, 4) for _ in range(1, 10)]
        # moves = map(lambda x: self._actions[x], ind)
        # moves = list(map(lambda x: self._actions[x], ind))
        moves = [self._actions[x] for x in ind]
        moves.append('drop')

        return moves
