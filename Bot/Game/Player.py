# -*- coding: utf-8 -*-
# Python3.4*

from Bot.Game.Field import Field


class Player:
    def __init__(self, name=None):
        self.name = name
        self.rowPoints = 0
        self.combo = 0

        self.field = Field()

    def updateRowPoints(self, rowPoints):
        self.rowPoints = rowPoints

    def updateCombo(self, combo):
        self.combo = combo
