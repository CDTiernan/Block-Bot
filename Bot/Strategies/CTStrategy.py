# -*- coding: utf-8 -*-
# Python3.4*

from random import randint
from Bot.Strategies.AbstractStrategy import AbstractStrategy
from Bot.Game.Field import Field
import time

'''
    My most simple and first implementation. It looks one block ahead and used projectPieceDown
'''
class CTStrategy(AbstractStrategy):
    def __init__(self, game):

        AbstractStrategy.__init__(self, game)
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']

    def choose(self):
        moves = []

        cur_field = self._game.me.field
        piece = self._game.piece
        piece_pos = self._game.piecePosition
        next_piece = self._game.nextPiece

        backup_field = cur_field.field
        max_score = -100000
        best_piece_rotation = None
        best_piece_position = None

        # loop through all the first piece rotations
        for piece_rotations in range(len(piece._rotations)):
            # and all the first piece positoins (x only cuz projecting down)
            for piece_positions in range(-2,cur_field.width):

                # project and test if valid field
                test_field = cur_field.projectPieceDown(piece, [piece_positions,0])
                if test_field:

                    score = self.calculate_field_score(test_field)

                    if score > max_score:
                        max_score = score
                        best_piece_rotation = piece_rotations
                        best_piece_position = piece_positions

            # turn the first piece once
            piece.turnRight(times=1)


        for _ in range(best_piece_rotation):
            moves.append('turnright')

        position_diff = piece_pos[0] - best_piece_position
        for _ in range(position_diff):
            if position_diff < 0:
                moves.append('right')
            elif position_diff > 0:
                moves.append('left')


        moves.append('drop')

        return moves

    def calculate_field_score(self, possible_field):
        score = 0

        holes, complete_lines, total_height, bumpiness = self.get_features(possible_field)

        score = -0.510066 * total_height + 0.760666 * complete_lines + -0.35663 * holes + -0.184483 * bumpiness
        return score

    def get_features(self,possible_field):
        width = len(possible_field[0])
        height = len(possible_field)

        reversed_field = possible_field[::-1]

        holes = 0.0
        complete_lines = 0.0
        total_height = 0.0
        bumpiness = 0.0

        cur_height = [0]*width
        for y in range(height):
            complete = True
            for x in range(width):

                if reversed_field[y][x] in (2,4):
                    if y+1 >= (cur_height[x] + 2):
                        holes += 1

                    cur_height[x] = y+1

                else:
                    complete = False

            if complete:
                complete_lines += 1

        total_height = sum(cur_height)

        for x in range(len(cur_height)-1):
            bumpiness += abs(cur_height[x]-cur_height[x+1])

        return holes, complete_lines, total_height, bumpiness
