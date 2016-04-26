# -*- coding: utf-8 -*-
# Python3.4*

from sys import stdin, stdout, argv

from Bot import Planner
from Bot.Game.Game import Game
from Bot.Parser import Parser


class Bot:
    def __init__(self, strategy, params):
        self.game = Game()
        self._parser = Parser(self.game)
        self._planner = Planner.create(strategy, self.game, params)

    def run(self):
        while not stdin.closed:
            try:
                line = stdin.readline().strip()

                if len(line) == 0:
                    continue

                moves = self.interpret(line)

                if moves:
                    self.sendMoves(moves)

            except EOFError:
                return

    def interpret(self, line):
        if line.startswith('action'):
            return self._planner.makeMove()
        else:
            self._parser.parse(line)

    @staticmethod
    def sendMoves(moves):
        stdout.write(','.join(moves) + '\n')
        stdout.flush()


if __name__ == '__main__':
    #TODO: get params from terminals
    params = {
        'height_weight' : -0.510066,
        'lines_weight' : 0.760666,
        'holes_weight' : -0.35663,
        'bumpiness_weight' : -0.184483,
        'valleys_weight' : 3.0,
        'name' : 'default'
    }
    for arg in argv[1:]:
        arg_array = arg.split("=",2)

        if arg_array[0] == "height_weight":
            params['height_weight'] = float(arg_array[1])

        if arg_array[0] == "line_weight":
            params['lines_weight'] = float(arg_array[1])

        if arg_array[0] == "holes_weight":
            params['holes_weight'] = float(arg_array[1])

        if arg_array[0] == "bumpiness_weight":
            params['bumpiness_weight'] = float(arg_array[1])

        if arg_array[0] == "valleys_weight":
            params['valleys_weight'] = float(arg_array[1])

        if arg_array[0] == "name":
            params['name'] = str(arg_array[1])

    #print(params)
    Bot("ctstratquick",params).run()
