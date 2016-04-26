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
import threading
from queue import Queue
from collections import OrderedDict

class CTStrategyEfficientMoves(AbstractStrategy):
    def __init__(self, game, params):
        # set up #loggin file for strategy

        self.log = open("stratOut.txt", 'w')

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


        self.possible_fields = {}
        self.fields = []

        # lock to serialize console output
        self.lock = threading.Lock()
        self.q = Queue()


        self.height_weight = params['height_weight']
        self.holes_weight = params['holes_weight']
        self.lines_weight = params['lines_weight']
        self.bumpiness_weight = params['bumpiness_weight']
        self.valleys_weight = params['valleys_weight']


        self.log.write("Strategy Output:\n\n")
        self.log.close()

    # def do_work(self, field):
    #     possible_field = copy.deepcopy(self.memorized_field)
    #     possible_field.updateField(field)
    #
    #     next_piece_fields = self.get_possible_fields(self._game.nextPiece, possible_field)
    #
    #     for next_piece_field in next_piece_fields:
    #         score = self.calculate_field_score(next_piece_field)
    #         with self.lock:
    #             if score not in self.possible_fields:
    #                 self.possible_fields[score] = []
    #
    #             self.possible_fields[score].append(next_piece_field.field)
    #
    # # The worker thread pulls an item from the queue and processes it
    # def worker(self):
    #     while True:
    #         self.log.write('fiid')
    #         field = self.q.get()
    #         self.do_work(field)
    #         self.q.task_done()

    def find_rotation_fields(self, params):
        piece = params.piece
        field = params.field

        feilds = []
        tested_columns = []
        piece_y_lims = piece.get_y_pos_lims()
        for piece_y in range(field.height + piece_y_lims[0], piece_y_lims[1],-1):

            piece_x_lims = piece.get_x_pos_lims()
            for piece_x in range(piece_x_lims[0],piece_x_lims[1]):
                if piece_x not in tested_columns:
                    test_field = field.projectPiece(piece, [piece_x,piece_y])

                    if test_field:
                        fields.append(test_field)
                        tested_columns.append(piece_x)

        return fields


    # The worker thread pulls an item from the queue and processes it
    def rotation_worker(self):
        while True:
            self.log.write('rworker')
            params = self.q.get()
            self.fields += self.find_rotation_fields(params)
            self.q.task_done()


    def choose(self):
        try:
            self.log = open("stratOut.txt", 'a')
            t0 = time.time()
            self.log.write("ROUND:  "+str(self._game.round)+"\n")

            cur_field = self._game.me.field
            self.memorized_field = copy.deepcopy(cur_field)
            piece = self._game.piece
            piece_pos = self._game.piecePosition
            next_piece = self._game.nextPiece
            game_round = self._game.round


            #self.log.write('fiid')
            # stuff work items on the queue (in this case, just a number).
            #start = time.perf_counter()
            #for item in range(20):
                #self.q.put(item)

            # Create the queue and thread pool.
            # for i in range(24):
            #      t = threading.Thread(target=self.worker)
            #      t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
            #      t.start()
            #
            #
            # self.possible_fields = {}
            #
            # piece_fields = self.get_possible_fields(piece,self.memorized_field)
            # for piece_field in piece_fields:
            #
            #     self.log.write('fiid')
            #     self.q.put(piece_field)
            #
            # self.q.join()       # block until all tasks are done

            #self.log.write(str(len(self.possible_fields)))

            # t1 = time.time()
            # self.log.write(str(t1-t0)+"\n")

            #od =  OrderedDict(sorted(self.possible_fields.items(), key=lambda t: t[0]))
            #for (score,field) in od.items():
            #    self.log.write(self.memorized_field.toString(field)+"\n")


            self.log.write("  Get All Game Board Configs \n")
            '''
            Try all possible piece and next piece rotations
            '''

            #if game_round == 1:

            self.get_possible_fields(piece,self.memorized_field)

            for piece_field in self.fields:
                self.log.write(self.memorized_field.toString(piece_field)+"\n")

                # self.memorized_field.updateField(piece_field)

                # next_piece_fields = self.get_possible_fields(next_piece,self.memorized_field)
                # for next_piece_field in next_piece_fields:
                #     score = self.calculate_field_score(next_piece_field)
                #     #self.log.write(self.memorized_field.toString(next_piece_field)+"\n")
                #
                #     if score not in self.possible_fields:
                #         self.possible_fields[score] = []
                #
                #     self.possible_fields[score].append(next_piece_field)
                #
                #
                # self.memorized_field.updateField(cur_field)


            t1 = time.time()
            self.log.write("    time: "+str(t1-t0)+"\n")


            self.log.write("  Get Moves to Best Possible Field \n")

            '''
            Handle talking to server
            '''

            moves = []
            '''
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
            '''
            moves.append('drop')

            self.log.close()
            return moves

        except:
            self.log.write("\n\nUnexpected error:\n"+sys.exc_info()[0]+"\n\n")

            self.log.close()
            return moves.append('no_moves')

    def get_possible_fields(self, piece, field):
        #fields = []

        # Create the queue and thread pool.
        for _ in range(len(piece._rotations)):
            t = threading.Thread(target=self.rotation_worker)
            t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
            t.start()

            params = { 'piece': piece, 'field': field }
            self.q.put(params)

            piece.turnRight(times=1)

        self.q.join()


    # def get_possible_fields(self, piece, field):
    #     fields = []
    #     for piece_r in range(len(piece._rotations)):
    #
    #         tested_columns = []
    #         piece_y_lims = piece.get_y_pos_lims()
    #         for piece_y in range(field.height + piece_y_lims[0], piece_y_lims[1],-1):
    #
    #             piece_x_lims = piece.get_x_pos_lims()
    #             for piece_x in range(piece_x_lims[0],piece_x_lims[1]):
    #                 if piece_x not in tested_columns:
    #                     test_field = field.projectPiece(piece, [piece_x,piece_y])
    #
    #                     if test_field:
    #                         fields.append(test_field)
    #                         tested_columns.append(piece_x)
    #
    #         piece.turnRight(times=1)


        return fields

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


        score = self.height_weight * height+ self.lines_weight * point_getting_lines + self.holes_weight * holes + self.bumpiness_weight * bumpiness + self.valleys_weight * has_valley

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

        #self.log.write(str(total_height)+" ")
        #self.log.write(str(total_holes)+" ")
        #self.log.write(str(total_bumpiness)+" ")
        #self.log.write(str(total_lines)+" ")
        #self.log.write(str(total_valleys)+"\n")

        return total_height, total_holes, total_bumpiness, total_lines, total_valleys

    # def get_features(self,possible_field):
    #     width = len(possible_field[0])
    #     height = len(possible_field)
    #
    #     reversed_field = possible_field[::-1]
    #
    #     holes = 0.0
    #     complete_lines = 0.0
    #     total_height = 0.0
    #     bumpiness = 0.0
    #
    #     cur_height = [0]*width
    #     for y in range(height):
    #         complete = True
    #         if sum(reversed_field[y]) != 0:
    #             for x in range(width):
    #
    #                 if reversed_field[y][x] in (2,4):
    #                     if y+1 >= (cur_height[x] + 2):
    #                         holes += 1
    #
    #                     cur_height[x] = y+1
    #
    #                 else:
    #                     complete = False
    #
    #             if complete:
    #                 complete_lines += 1
    #
    #     total_height = sum(cur_height)
    #
    #     for x in range(len(cur_height)-1):
    #         bumpiness += abs(cur_height[x]-cur_height[x+1])
    #
    #     return holes, complete_lines, total_height, bumpiness
