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
            #t0 = time.time()

            cur_field = self._game.me.field
            piece = self._game.piece
            piece_pos = self._game.piecePosition
            next_piece = self._game.nextPiece
            game_round = self._game.round
            self.log.write("\nround "+str(game_round)+"\n")

            self.log.write(cur_field.toString(cur_field.field))

            '''
            Handle First Piece
            '''
            # first piece is always dropped immediately
            if game_round == 1:
                # make a static copy of the field
                self.memorized_field = copy.deepcopy(cur_field)

                best_offset = piece_pos
                best_nudge_offset = piece_pos
                best_piece_rotation = 0

                # update the playing field
                x_pos = piece_pos[0]
                test_field = self.memorized_field.projectPieceDown(piece, [x_pos,0])
                self.memorized_field.updateField(test_field)

            # the next piece is calculated one move in advance so simply get the moves
            else:
                self.memorized_field = copy.deepcopy(cur_field)

                best_offset = self.best_next_offset
                best_nudge_offset = self.best_next_nudge_offset
                best_piece_rotation = self.best_next_piece_rotation
                best_piece = self.best_next_piece

                test_field, offset = self.memorized_field.get_pojected_piece_offset(best_piece,[best_offset[0],0])

                self.memorized_field.updateField(test_field)


            '''
            Handle Second Piece
            '''
            best_field = None
            best_score = -100000

            # loop through all the next piece positions and rotatoins
            for next_piece_rotation in range(len(next_piece._rotations)):
                # randomly shuffle which columns to test (increases the distribution of peices)
                rand_cols = list(range(-1,self.memorized_field.width+1))
                random.shuffle(rand_cols)
                for next_piece_position in rand_cols:
                    test_field, offset = self.memorized_field.get_pojected_piece_offset(next_piece, [next_piece_position,0])

                    if test_field:
                        score = self.calculate_field_score(test_field)

                        proj_field = self.memorized_field.projectPieceDown(next_piece, [next_piece_position,0])

                        possible = True
                        nudge_offset = offset
                        if test_field != proj_field:
                            possible = False
                            for direction in (-1,1):
                                for nudge in range(1,self.memorized_field.width+1):
                                    possible_nudge_offset = [offset[0]+(nudge*direction), offset[1]]
                                    nudge_field = self.memorized_field.fitPiece(next_piece.positions(),possible_nudge_offset)

                                    if nudge_field:
                                        proj_field = self.memorized_field.projectPieceDown(next_piece, possible_nudge_offset)
                                        if (nudge_field == proj_field):
                                            nudge_offset = possible_nudge_offset
                                            possible = True
                                    else:
                                        break

                        if (score > best_score) and possible:
                            best_field = test_field
                            best_score = score
                            self.best_next_offset = offset
                            self.best_next_nudge_offset = nudge_offset
                            self.best_next_piece_rotation = next_piece_rotation
                            self.best_next_piece = copy.deepcopy(next_piece)

                # turn the next piece once
                next_piece.turnRight(times=1)

            self.memorized_field.updateField(best_field)

            self.log.write(self.memorized_field.toString(self.memorized_field.field))


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
