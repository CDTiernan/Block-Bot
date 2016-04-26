# -*- coding: utf-8 -*-
# Python3.4*

import copy


class Field:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.field = [[0]*self.width]*self.height

    def size(self):
        return self.width, self.height

    def updateField(self, field):
        self.field = field

    def projectPiece(self, piece, offset):
        piecePositions = self.__offsetPiece(piece.positions(), [offset[0],offset[1]])

        field = self.fitPiece(piecePositions, [0, 0])
        
        return field

    def projectPieceDown(self, piece, offset):
        piecePositions = self.__offsetPiece(piece.positions(), offset)

        field = None
        for height in range(0, self.height-1):
            tmp = self.fitPiece(piecePositions, [0, height])

            if not tmp:
                break
            field = tmp

        return field

    def get_pojected_piece_offset(self, piece, offset):
        piecePositions = self.__offsetPiece(piece.positions(), offset)

        field = None
        offset_x = offset[0]
        offset_y = 0
        for height in range(self.height, -1, -1):
            tmp = self.fitPiece(piecePositions, [0, height])

            if tmp:
                field = tmp
                offset_y = height
                break

        return field, [offset_x, offset_y]

    @staticmethod
    def __offsetPiece(piecePositions, offset):
        piece = copy.deepcopy(piecePositions)
        for pos in piece:
            pos[0] += offset[0]
            pos[1] += offset[1]

        return piece

    def __checkIfPieceFits(self, piecePositions):
        for x, y in piecePositions:
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.field[y][x] > 1:
                    return False
            else:
                return False
        return True

    def __check_if_piece_fits_snug(self, piecePositions):
        for x, y in piecePositions:
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.field[y][x] > 1:
                    return False
            else:
                return False
        return True

    def fitPiece(self, piecePositions, offset=None):
        if offset:
            piece = self.__offsetPiece(piecePositions, offset)
        else:
            piece = piecePositions

        field = copy.deepcopy(self.field)
        if self.__checkIfPieceFits(piece):
            for x, y in piece:
                field[y][x] = 4

            return field
        else:
            return None

    def toString(self, f):
        stringField = ''
        for row in f:
            #if 2 in row or 4 in row or 3 in row:
            for element in row:
                stringField += str(element)+' '
            stringField += '\n'
        stringField += '\n'

        return stringField
