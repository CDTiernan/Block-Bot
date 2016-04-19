# -*- coding: utf-8 -*-
# Python3.4*

from random import randint
from Bot.Strategies.AbstractStrategy import AbstractStrategy
from Bot.Game.Field import Field
from multiprocessing import Pool
import time

class CTStrategyTwoBlock(AbstractStrategy):
    def __init__(self, game):
        # set up loggin file for strategy
        #log = open("stratOut.txt", 'w')
        #log.write("INIT")
        #log.close()

        AbstractStrategy.__init__(self, game)
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']
        self.memorized_field = game.me.field.field

    def choose(self):
        #log = open("stratOut.txt", 'a')

        #t0 = time.time()
        #log.write("t0: "+ str(t0-t0)+"\n")

        #to_write = "ROUND: " + str(self._game.round) + "\n"
        #log.write(to_write)

        moves = []

        cur_field = self._game.me.field
        piece = self._game.piece
        piece_pos = self._game.piecePosition
        next_piece = self._game.nextPiece


        #to_write = cur_field.toString(self.memorized_field)
        #log.write(to_write)

        backup_field = cur_field.field
        max_score = -100000
        best_piece_rotation = None
        best_piece_position = None
        best_next_piece_rotation = None
        best_next_piece_position = None


        #t1 = time.time()
        #log.write("t1: "+ str(t1-t0)+"\n")

        #pool = Pool()
        #fields = []
        # loop through all the first piece rotations
        for piece_rotations in range(len(piece._rotations)):
            # and all the first piece positoins (x only cuz projecting down)
            for piece_positions in range(-2,cur_field.width):

                # project and test if valid field
                test_field = cur_field.projectPieceDown(piece, [piece_positions,0])
                if test_field:
                    # update the field to place second piece
                    cur_field.updateField(test_field)

                    # loop through all the next piece rotations
                    for next_piece_rotations in range(len(next_piece._rotations)):
                        # and all the next piece positions (only x again)
                        for next_piece_positions in range(-2,cur_field.width):

                            # test if valid field
                            test_field = cur_field.projectPieceDown(next_piece, [next_piece_positions,0])
                            if test_field:
                                #log.write(cur_field.toString(test_field))

                                # get score of possible board layout
                                score = self.calculate_field_score(test_field)
                                #fields.append(np.array(test_field))

                                #log.write(str(score)+" "+str(max_score)+"\n")

                                if score > max_score:
                                    max_score = score
                                    best_piece_rotation = piece_rotations
                                    best_piece_position = piece_positions
                                    best_next_piece_rotation = next_piece_rotations
                                    best_next_piece_position = next_piece_positions
                                    self.memorized_field = test_field

                        # turn the next piece once
                        next_piece.turnRight(times=1)

                    # revert to current board layout to try next first piece place
                    cur_field.updateField(backup_field)

            # turn the first piece once
            piece.turnRight(times=1)


        t2 = time.time()
        #log.write("t2: "+ str(t2-t0)+"\n")

        for _ in range(best_piece_rotation):
            #log.write("turning right\n\n")
            moves.append('turnright')


        t3 = time.time()
        #log.write("t3: "+ str(t3-t0)+"\n")

        position_diff = piece_pos[0] - best_piece_position
        position_abs_diff = abs(position_diff)
        for _ in range(position_abs_diff):
            if position_diff < 0:
                moves.append('right')
            elif position_diff > 0:
                moves.append('left')


        #t4 = time.time()
        #log.write("t4: "+ str(t4-t0)+"\n\n")

        # always drop at end of turn
        moves.append('drop')

        #log.write("t2: "+str(t2)+"\n")

        #log.close()
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
