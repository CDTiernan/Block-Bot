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
    # default parameters using which the bot will score board states
    params = {
        'height_weight' : -2.93969377104926,
        'lines_weight' : 1.8838043309144208,
        'holes_weight' : -1.0982709295643653,
        'bumpiness_weight' : -0.5442373651415795,
        'valleys_weight' : 1.4400243626054037,
        'name' : 'default'
    }
    # gets args from the console command (if they exist) and overwrites default parameters
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

    # define parameters and strategy to use
    Bot("ct2b",params).run()
