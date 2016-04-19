# -*- coding: utf-8 -*-
# Python3.4*

from random import randint
from Bot.Strategies.AbstractStrategy import AbstractStrategy
from Bot.Game.Field import Field
import time

class CTStrategy(AbstractStrategy):
    def __init__(self, game):
        # set up loggin file for strategy
        #log = open("stratOut.txt", 'w')
        #log.close()

        AbstractStrategy.__init__(self, game)
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']

    def choose(self):
        #log = open("stratOut.txt", 'a')

        #t0 = time.time()

        t0 = time.time()
        log.write("t0: "+ str(t0-t0)+"\n\n")
        #to_write = "ROUND: " + str(self._game.round) + "\n"
        #log.write(to_write)

        moves = []

        cur_field = self._game.me.field
        piece = self._game.piece
        piece_pos = self._game.piecePosition
        next_piece = self._game.nextPiece


        #to_write = cur_field.toString(cur_field.field)
        #log.write(to_write)


        t2 = time.time()
        log.write("t2: "+ str(t2-t0)+"\n\n")

        backup_field = cur_field.field
        max_score = -100000
        best_piece_rotation = None
        best_piece_position = None
        #best_next_piece_rotation = None
        #best_next_piece_position = None
        # loop through all the first piece rotations
        for piece_rotations in range(len(piece._rotations)):
            # and all the first piece positoins (x only cuz projecting down)
            for piece_positions in range(-2,cur_field.width):

                # project and test if valid field
                test_field = cur_field.projectPieceDown(piece, [piece_positions,0])
                if test_field:

                    score = self.calculate_field_score(test_field)

                    #log.write(str(score)+" "+str(max_score)+"\n")

                    if score > max_score:
                        max_score = score
                        best_piece_rotation = piece_rotations
                        best_piece_position = piece_positions

            # turn the first piece once
            piece.turnRight(times=1)


        t3 = time.time()
        log.write("t3: "+ str(t3-t0)+"\n\n")

        #t1 = time.time() - t0
        #log.write("t1: "+str(t1)+"\n")
        #log.write(str(best_piece_rotation) + "\n\n")
        #log.write(str(best_piece_position) + "\n\n")
        for _ in range(best_piece_rotation):
            #log.write("turning right\n\n")
            moves.append('turnright')
            #log.write("turning right\n\n")

        #log.write("pdiff: "+str(piece_pos[0]))
        position_diff = piece_pos[0] - best_piece_position
        #log.write(str(position_diff)+"\n")
        for _ in range(position_diff):
            if position_diff < 0:
                moves.append('right')
            elif position_diff > 0:
                moves.append('left')


        t4 = time.time()
        log.write("t4: "+ str(t4-t0)+"\n\n")

        # always drop at end of turn
        moves.append('drop')

        #t2 = time.time() - t0
        #log.write("t2: "+str(t2)+"\n")

        #log.close()
        return moves

    def calculate_field_score(self, possible_field):
        score = 0
        #log.write("1\n")

        #tot_height = self.get_total_height(possible_field)
        #complete_lines = self.get_complete_lines(possible_field)
        #holes = self.get_number_holes(possible_field)
        #bumpiness = self.get_bumpiness(possible_field)
        holes, complete_lines, total_height, bumpiness = self.get_features(possible_field)
        #print("holes %i, lines %i, height %i, bumpiness %i", (holes, complete_lines, total_height, bumpiness))

        #score = str(holes) + " " + str(complete_lines) + " " + str(total_height) + " " + str(bumpiness)
        score = -0.510066 * total_height + 0.760666 * complete_lines + -0.35663 * holes + -0.184483 * bumpiness
        #log.write("2\n")
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
