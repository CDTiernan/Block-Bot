# -*- coding: utf-8 -*-
# Python3.4*

from random import randint
from Bot.Strategies.AbstractStrategy import AbstractStrategy
from Bot.Game.Field import Field
import time
import copy
import sys
from heapq import heappop, heappush, nlargest
from Bot.Game.TetrisGraph import Graph
# import threading
# from queue import Queue
# from collections import OrderedDict

class CTStrategyEfficientMoves(AbstractStrategy):
    def __init__(self, game, params):
        # set up #loggin file for strategy

        #self.log = open("stratOut.txt", 'w')
        self.game_time = time.time()

        AbstractStrategy.__init__(self, game)

        self.memorized_field = None
        self.col_heights = [0]*game.me.field.width


        self.height_weight = params['height_weight']
        self.holes_weight = params['holes_weight']
        self.lines_weight = params['lines_weight']
        self.bumpiness_weight = params['bumpiness_weight']
        self.valleys_weight = params['valleys_weight']

        # self.log.write("Strategy Output:\n\n")
        #self.log.close()

    def choose(self):
        try:
            #self.log = open("stratOut.txt", 'a')
            t0 = time.time()
            #self.log.write("ROUND:  "+str(self._game.round)+"\n")

            cur_field = self._game.me.field
            self.memorized_field = copy.deepcopy(cur_field)
            piece = self._game.piece
            piece_pos = self._game.piecePosition
            next_piece = self._game.nextPiece
            game_round = self._game.round



            t1 = time.time()

            #self.log.write("  Get All Game Board Configs \n")
            '''
            Try all possible piece and next piece rotations
            '''

            if game_round != 1:
                self.get_col_heights(self.memorized_field.field)


            if True:

                next_state_data = []

                piece_fields, piece_offsets, piece_rotations = self.get_possible_fields_offsets(piece,self.memorized_field)

                for piece_idx in range(len(piece_fields)):

                    piece_offset = piece_offsets[piece_idx]
                    piece_field = piece_fields[piece_idx]
                    piece_rotation = piece_rotations[piece_idx]

                    self.memorized_field.updateField(piece_field)
                    self.get_col_heights(self.memorized_field.field)

                    next_piece_fields, next_piece_offsets, next_piece_rotations = self.get_possible_fields_offsets(next_piece,self.memorized_field)
                    for next_piece_idx in range(len(next_piece_fields)):

                        next_piece_offset = next_piece_offsets[next_piece_idx]
                        next_piece_field = next_piece_fields[next_piece_idx]
                        next_piece_rotation = next_piece_rotations[next_piece_idx]

                        score = self.calculate_field_score(next_piece_field)
                        params = [piece_field, piece, piece_offset, next_piece_field, next_piece, next_piece_offset, piece_rotation]

                        heappush(next_state_data, (score, params))


                    self.memorized_field.updateField(cur_field.field)

            t2 = time.time()
            #self.log.write("    Calculate moves time: "+str(t2-t1)+"\n")


            #self.log.write("  Get Moves to Best Possible Field \n")
            '''
            Handle finding best moves
            '''
            #self.log.write(self.memorized_field.toString(self.memorized_field.field))

            moves = []
            for (score,params) in nlargest(25, next_state_data):
                #self.log.write("  Itterating through best fields\n")
                moves = self.escape_piece(params)
                #self.log.write(str(score)+'====\n')
                if moves:
                    #self.log.write("  found moves \n")
                    #self.log.write(self.memorized_field.toString(params[0]))
                    #self.log.write(str(moves)+"\n")
                    break


            moves.append('drop')

            t3 = time.time()
            #self.log.write("    Find best moves time: "+str(t3-t2)+"\n")


            #self.log.write("Total round time: "+str(t3-t0)+"\n")
            #self.log.write("Total game time: "+str(t3-self.game_time)+"\n\n")

            #self.log.close()

            return moves

        except:
            #self.log.write("\n\nUnexpected error:\n"+sys.exc_info()[0]+"\n\n")

            #self.log.close()
            return moves.append('no_moves')

    def escape_piece(self, params):
        moves = []
        #self.log.write("  1\n")

        cur_offset = self._game.piecePosition
        cur_rotation = 0

        piece_field = params[0]
        piece = params[1]
        piece_offset = params[2]
        piece_rotation = params[6]
        # self.log.write("  2\n")

        next_piece_field = params[3]
        next_piece = params[4]
        next_piece_offsett = params[5]
        next_piece_rotation = next_piece._rotateIndex

        # self.log.write("  3\n")
        g = Graph(list(cur_offset), cur_rotation, piece_offset, piece_rotation, self.memorized_field, piece)
        # self.log.write("  4\n")
        moves = g.escape()
        # self.log.write(str(moves)+"  5\n")

        return moves

    def get_possible_fields_offsets(self, piece, field):
        fields = []
        piece_offsets = []
        piece_rotations = []

        for piece_r in range(len(piece._rotations)):

            piece_x_lims = piece.get_x_pos_lims()
            piece_x_check_pos = piece.get_x_check_pos()
            for piece_x in range(piece_x_lims[0],piece_x_lims[1]):
                col_to_check = piece_x + (self.memorized_field.width - piece_x_check_pos[1])
                col_height = self.col_heights[col_to_check]

                piece_y_lims = piece.get_y_pos_lims()
                y_min = field.height + piece_y_lims[0] - col_height
                for piece_y in range(y_min, piece_y_lims[1],-1):
                    test_field = field.projectPiece(piece, [piece_x,piece_y])

                    if test_field:
                        fields.append(test_field)
                        piece_offsets.append([piece_x,piece_y])
                        piece_rotations.append(piece._rotateIndex)
                        break

            piece.turnRight(times=1)

        # piece_reset = len(piece._rotations) - 1
        # piece.turnLeft(time=piece_reset)

        return fields, piece_offsets, piece_rotations



    def calculate_field_score(self, possible_field):
        score = 0

        height, holes, bumpiness, lines, valleys = self.get_features(possible_field)
        point_getting_lines = lines - 1

        if valleys == 0:
            has_valley = 0
        elif valleys == 1:
            has_valley = 1
        else:
            has_valley = -1


        score = self.height_weight * height+ self.lines_weight * point_getting_lines + self.holes_weight * holes + self.bumpiness_weight * bumpiness

        return score

    def get_features(self,possible_field):
        width = len(possible_field[0])
        height = len(possible_field)


        total_height = 0
        total_holes = 0
        total_bumpiness = 0

        last_col_height = -1
        filled_row_counter = [0] * height

        total_valleys = 0
        possible_valley = True
        for x in range(width):
            col_height = 0
            col_holes = 0
            last_cell_empty = 0
            for y in range(height-1,-1,-1):
                elem = possible_field[y][x]
                if elem > 1:
                    if last_cell_empty:
                        col_holes += last_cell_empty

                    col_height = height-y

                    if elem != 3:
                        filled_row_counter[y] += 1

                    last_cell_empty = 0
                else:
                    last_cell_empty += 1

            self.col_heights[x] = col_height

            total_height += col_height
            total_holes += col_holes

            if last_col_height != -1:
                total_bumpiness += abs(last_col_height-col_height)

                if possible_valley and last_col_height-col_height <= -3:
                    total_valleys += 1
                    possible_valley = False

                if last_col_height-col_height >= 3:
                    possible_valley = True
                else:
                    possible_valley = False

            last_col_height = col_height

        if possible_valley:
            total_valleys += 1

        total_lines = 0
        for num_elems in filled_row_counter:
            if num_elems == width:
                total_lines += 1

        return total_height, total_holes, total_bumpiness, total_lines, total_valleys

    def get_col_heights(self,possible_field):
        width = len(possible_field[0])
        height = len(possible_field)

        for x in range(width):
            col_height = 0
            for y in range(height-1,-1,-1):
                elem = possible_field[y][x]
                if elem > 1:
                    col_height = height-y

            self.col_heights[x] = col_height
