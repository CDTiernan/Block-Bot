# -*- coding: utf-8 -*-
# Python3.4*

from random import randint
from Bot.Strategies.AbstractStrategy import AbstractStrategy
from Bot.Game.Field import Field
from multiprocessing import Pool
import random
import time
import copy
import sys

class CTStrategyPreferred(AbstractStrategy):
    def __init__(self, game, params):
        # set up #loggin file for strategy

        self.log = open("stratOut.txt", 'w')
        self.log.write("Strategy Output:\n\n")
        self.log.close()

        AbstractStrategy.__init__(self, game)
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']

        #self.best_next_piece_rotation = None
        #self.best_next_piece_position = None

        self.best_next_offset = None
        self.best_next_nudge_offset = None
        self.best_next_rotation = None
        self.best_next_nudge_rotation = None
        self.best_next_piece = None
        self.memorized_field = None
        self.enemy_points = 0

        self.height_weight = params['height_weight']
        self.holes_weight = params['holes_weight']
        self.lines_weight = params['lines_weight']
        self.bumpiness_weight = params['bumpiness_weight']

    def choose(self):
        try:
            self.log = open("stratOut.txt", 'a')
            t0 = time.time()

            cur_field = self._game.me.field
            piece = self._game.piece
            piece_pos = self._game.piecePosition
            next_piece = self._game.nextPiece
            game_round = self._game.round

            self.log.write("\nround "+str(game_round)+"\n")


            # make a copy of the current field
            self.memorized_field = copy.deepcopy(cur_field)

            f = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 2, 2, 2, 2, 2, 2, 2, 2, 2], [0, 2, 2, 2, 2, 2, 2, 2, 2, 2], [0, 2, 2, 2, 2, 2, 2, 2, 2, 2], [0, 2, 2, 2, 2, 2, 2, 2, 2, 2], [0, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

            self.memorized_field.updateField(f)

            #self.log.write(self.memorized_field.toString(self.memorized_field.field))

            '''
            Try all possible piece and next piece rotations
            '''
            possible_fields = {}
            best_score = -100000

            t1 = time.time()
            self.log.write("start: "+ str(t1-t0))

            # loop through all the next piece positions and rotatoins
            for piece_rotation in range(len(piece._rotations)):

                # randomly shuffle which columns to test (increases the distribution of peices)
                rand_cols = list(range(-3,self.memorized_field.width))
                #random.shuffle(rand_cols)
                for piece_position in rand_cols:
                    test_field, offset = self.memorized_field.get_pojected_piece_offset(piece, [piece_position,0])
                    #self.log.write(str(offset)+"\n")
                    if test_field:
                        self.memorized_field.updateField(test_field)

                        # loop through all the next piece positions and rotatoins
                        for next_piece_rotation in range(len(next_piece._rotations)):

                            # randomly shuffle which columns to test (increases the distribution of peices)
                            next_rand_cols = list(range(-3,self.memorized_field.width))
                            #random.shuffle(next_rand_cols)
                            for next_piece_position in next_rand_cols:
                                next_test_field, next_offset = self.memorized_field.get_pojected_piece_offset(next_piece, [next_piece_position,0])


                                if next_test_field:
                                    ##self.log.write('TEST FIELD\n')
                                    self.log.write(self.memorized_field.toString(next_test_field))
                                    #score = self.calculate_field_score(next_test_field)

                                    #if score not in possible_fields.keys():
                                    #    possible_fields[score] = []

                                    #possible_fields[score].append(
                                    #{
                                    #    'best_piece_offset': offset,
                                    #    'best_piece_rotation': piece_rotation,
                                    #    'best_next_piece_offset': next_offset,
                                    #    'best_next_piece_rotation': next_piece_rotation
                                    #})


                            self.memorized_field.updateField(test_field)
                            # turn the next piece once
                            next_piece.turnRight(times=1)

                    self.memorized_field.updateField(f)
                    # turn the piece once
                    piece.turnRight(times=1)



                t1 = time.time()
                self.log.write("end: "+ str(t1-t0))

            '''
            Handle talking to server
            '''
            moves = []

            rotations = best_piece_rotation
            for _ in range(rotations):
                moves.append('turnright')

            x_nudge_position_difference = best_nudge_offset[0] - piece_pos[0]
            for _ in range(abs(x_nudge_position_difference)):

                if x_nudge_position_difference<0:
                    moves.append('left')
                elif x_nudge_position_difference>0:
                    moves.append('right')

            y_nudge_position_difference = best_nudge_offset[1] - piece_pos[1]
            for _ in range(y_nudge_position_difference):
                moves.append('down')

            x_nudge_offset_difference = best_offset[0] - best_nudge_offset[0]
            for _ in range(abs(x_nudge_offset_difference)):
                if x_nudge_offset_difference<0:
                    moves.append('left')
                elif x_nudge_offset_difference>0:
                    moves.append('right')

            moves.append('drop')

            self.log.close()
            return moves

        except:
            self.log.write("\n\nUnexpected error:\n"+sys.exc_info()[0]+"\n\n")

            self.log.close()
            return moves.append('no_moves')

    def calculate_field_score(self, possible_field):
        score = 0

        holes, complete_lines, total_height, bumpiness = self.get_features(possible_field)

        score = self.height_weight * total_height + self.lines_weight * (complete_lines-1)**2 + self.holes_weight * holes + self.bumpiness_weight * bumpiness
        if complete_lines >= 3:
            score = 10000
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
            if sum(reversed_field[y]) != 0:
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
