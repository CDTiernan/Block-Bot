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

'''
 This is a strategy based off a hueristic that ranks possible field states based off extracted features and weights
 learned from a genetic algorithm. It takes into account both the falling piece and the next piece, trying
 every rotation and position for both pieces and placing them in a heap. After all possible fields are tested,
 the top scoring fields are then tested to see if the falling piece can be moved to the desired position on the board.
 Once a valid set of moves for the first piece have been found the move list is compiled and sent to the server.
'''

class CTStrategyTwoBlock(AbstractStrategy):
    def __init__(self, game, params):
        AbstractStrategy.__init__(self, game)

        self.memorized_field = None
        self.col_heights = [0]*game.me.field.width

        self.height_weight = params['height_weight']
        self.holes_weight = params['holes_weight']
        self.lines_weight = params['lines_weight']
        self.bumpiness_weight = params['bumpiness_weight']
        self.valleys_weight = params['valleys_weight']


    def choose(self):
        try:
            cur_field = self._game.me.field

            # update the memorized field
            self.memorized_field = copy.deepcopy(cur_field)

            piece = self._game.piece
            piece_pos = self._game.piecePosition
            next_piece = self._game.nextPiece
            game_round = self._game.round

            '''
            Try all possible piece and next piece rotations
            '''

            # if the game is past the first round get the column heights (used to pick where to place pieces)
            if game_round != 1:
                self.get_col_heights(self.memorized_field.field)


            next_state_data = []
            piece_fields, piece_offsets, piece_rotations = self.get_possible_fields_offsets(piece,self.memorized_field)
            # for all the possible field states based of the first piece
            for piece_idx in range(len(piece_fields)):
                # extract the piece info from the field
                piece_offset = piece_offsets[piece_idx]
                piece_field = piece_fields[piece_idx]
                piece_rotation = piece_rotations[piece_idx]

                # update the memorized_field to test the second piece
                self.memorized_field.updateField(piece_field)
                # get the column heights (used to pick where to place pieces)
                self.get_col_heights(self.memorized_field.field)

                next_piece_fields, next_piece_offsets, next_piece_rotations = self.get_possible_fields_offsets(next_piece,self.memorized_field)
                # for all the possible field states based of the second piece and the first piece
                for next_piece_idx in range(len(next_piece_fields)):
                    # extract the piece info from the field
                    next_piece_offset = next_piece_offsets[next_piece_idx]
                    next_piece_field = next_piece_fields[next_piece_idx]
                    next_piece_rotation = next_piece_rotations[next_piece_idx]

                    # calculate the score of the field
                    score = self.calculate_field_score(next_piece_field)

                    # compile all needed info and heappush it onto a list
                    params = [piece_field, piece, piece_offset, next_piece_field, next_piece, next_piece_offset, piece_rotation]
                    # heappush is used to keep order of all the fields by score (we want to escape the best fields first)
                    heappush(next_state_data, (score, params))

                # reset the memorized field so a new first piece block position can be tested
                self.memorized_field.updateField(cur_field.field)

            '''
            Handle finding best moves
            '''
            moves = None
            # get the top 25 scoring fields from the heap
            for (score,params) in nlargest(25, next_state_data):
                # escape the piece (get the moves needed to get the piece into position)
                moves = self.escape_piece(params)
                # if there are valid moves to get the piece to the desired position break the loop and tell the server
                if moves:
                    break

            # always drop the piece at the end of moves
            moves.append('drop')

            return moves

        except:
            return moves.append('no_moves')

    '''
     Uses the TetrisGraph to find out if the possible field is valid (aka there are a set of moves that
     can be executed to get the piece into the position desired on the field)
    '''
    def escape_piece(self, params):
        moves = []

        cur_offset = self._game.piecePosition
        cur_rotation = 0

        piece_field = params[0]
        piece = params[1]
        piece_offset = params[2]
        piece_rotation = params[6]

        next_piece_field = params[3]
        next_piece = params[4]
        next_piece_offsett = params[5]
        next_piece_rotation = next_piece._rotateIndex

        # initialized the graph with all the field and piece information
        g = Graph(list(cur_offset), cur_rotation, piece_offset, piece_rotation, self.memorized_field, piece)
        # if the graph can escape the piece moves will be set to a list of moves, otherwise it will be set to None
        moves = g.escape()

        return moves

    '''
     Itterates through all of the piece rotations and positions allowed on the board to find all possible
     states created by taking action on the piece
    '''
    def get_possible_fields_offsets(self, piece, field):
        fields = []
        piece_offsets = []
        piece_rotations = []

        # for all rotations
        for piece_r in range(len(piece._rotations)):
            # get the limits of movement for the piece and the lowest part of the piece (used to guess where it will fi or not)
            piece_x_lims = piece.get_x_pos_lims()
            piece_x_check_pos = piece.get_x_check_pos()
            # for all x positions the piece can take
            for piece_x in range(piece_x_lims[0],piece_x_lims[1]):
                # get the hieght of the column (to initially test at this hieght, not every height higher then traversing down)
                col_to_check = piece_x + (self.memorized_field.width - piece_x_check_pos[1])
                col_height = self.col_heights[col_to_check]

                piece_y_lims = piece.get_y_pos_lims()
                y_min = field.height + piece_y_lims[0] - col_height

                # for all y positions the piece can take
                for piece_y in range(y_min, piece_y_lims[1],-1):
                    # project the field. returns a valid field or None if the piece position is invalid
                    test_field = field.projectPiece(piece, [piece_x,piece_y])

                    # if the field is valid
                    if test_field:
                        # store the field, piece offset and rotation
                        fields.append(test_field)
                        piece_offsets.append([piece_x,piece_y])
                        piece_rotations.append(piece._rotateIndex)
                        break

            piece.turnRight(times=1)

        return fields, piece_offsets, piece_rotations


    '''
     This uses a hueristic to rank fields based on their features
     - complete_lines:
        - the number of full lines completed in the field (this only recieve points if there are more than 1 because no points are recieved for simply clearing 1 line)
     - height:
        - the total height of all the columns (including covered empty spaces)
     - holes:
        - the total number of covered empty spaces
     - bumpiness:
        - the sum off the column differences (left to right)
     - has_valley:
        - -1 if there is more than 1 valley of height 3+
        - 0 if there is no valley of height 3+
        - 1 if there is 1 valley of height 3+
    '''
    def calculate_field_score(self, possible_field, debug=False):
        score = 0

        # get the features
        height, holes, bumpiness, lines, valleys = self.get_features(possible_field)

        # one line clears do not recieve points so discount the feature
        point_getting_lines = lines - 1

        # convert the valleys feature into a 3 val variable
        if valleys == 0:
            has_valley = 0
        elif valleys == 1:
            has_valley = 1
        else:
            has_valley = -1

        # calculate score based off features and their weights
        score = self.height_weight * height+ self.lines_weight * point_getting_lines + self.holes_weight * holes + self.bumpiness_weight * bumpiness + self.valleys_weight * has_valley

        # if the move gets 3 or more lines, ALWAYS make it
        if lines >= 3:
            score = 10000

        return score

    '''
     Traverses a field, and extracts the needed features
    '''
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

    '''
     Paired down version of get_features() because column heights are needed more frequently than the other features
    '''
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
