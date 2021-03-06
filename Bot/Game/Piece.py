# -*- coding: utf-8 -*-
# Python3.4*


def create(type):
    switcher = {
        "L": LPiece(),
        "O": OPiece(),
        "I": IPiece(),
        "J": JPiece(),
        "S": SPiece(),
        "T": TPiece(),
        "Z": ZPiece()
    }

    return switcher.get(type.upper())


class Piece:
    def __init__(self):
        self._rotateIndex = 0
        self._rotations = []
        self._field_positions = []
        self._lowest_col_position = []

    def turnLeft(self, times=1):
        if self._rotateIndex > times-1:
            self._rotateIndex -= times
            return True
        return False

    def turnRight(self, times=1):
        if self._rotateIndex < len(self._rotations) - times:
            self._rotateIndex += times
            return True
        return False

    def rotateCount(self):
        return self._rotateIndex

    def positions(self):
        return self._rotations[self._rotateIndex]

    def get_x_pos_lims(self):
        # return [self._field_positions[self.rotateIndex][0][0],self._field_positions[self.rotateIndex][1][0]]
        return [self._field_positions[self._rotateIndex][0][0], 1+self._field_positions[self._rotateIndex][1][0]]
    def get_x_check_pos(self):
        # return [self._field_positions[self.rotateIndex][0][0],self._field_positions[self.rotateIndex][1][0]]
        return [self._lowest_col_position[self._rotateIndex][0][0], 1+self._lowest_col_position[self._rotateIndex][1][0]]

    def get_y_pos_lims(self):
        return [self._field_positions[self._rotateIndex][0][1], -1+self._field_positions[self._rotateIndex][1][1]]

    def appendRotation(self, rotation):
        self._rotations.append(rotation)

'''
    Each piece has a defined xy cords within a 4 by 4 box placed on the field. I added xy limits to each rotation and
    cords to the lowest part of the piece in each rotation
        self._rotations: the xy cordnates of the piece with respect to its rotation index
        self._field_positions: the x limits of a pieces movement on a field with respect to its rotation index
        self._lowest_col_position: the x coordnates of the pieces lowest piece with respect to its rotation index
'''
class LPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.type = "L"
        # rotations ordered by their rotation to the right
        self._rotations.append([[2, 0], [0, 1], [1, 1], [2, 1]])
        self._field_positions.append([[0,-2],[7,0]])
        self._lowest_col_position.append([[0,-2],[7,0]])

        self._rotations.append([[1, 0], [1, 1], [1, 2], [2, 2]])
        self._field_positions.append([[-1,-3],[7,0]])
        self._lowest_col_position.append([[-1,-3],[8,0]])

        self._rotations.append([[0, 1], [1, 1], [2, 1], [0, 2]])
        self._field_positions.append([[0,-3],[7,-1]])
        self._lowest_col_position.append([[0,-3],[9,-1]])

        self._rotations.append([[0, 0], [1, 0], [1, 1], [1, 2]])
        self._field_positions.append([[0,-3],[8,0]])
        self._lowest_col_position.append([[0,-3],[8,0]])


class OPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.type = "O"
        self._rotations.append([[0, 0], [1, 0], [0, 1], [1, 1]])
        self._field_positions.append([[0,-2],[8,0]])
        self._lowest_col_position.append([[0,-2],[9,0]])


class IPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.type = "I"
        # rotations ordered by their rotation to the right
        self._rotations.append([[0, 1], [1, 1], [2, 1], [3, 1]])
        self._field_positions.append([[0,-2],[6,-1]])
        self._lowest_col_position.append([[0,-2],[6,-1]])

        self._rotations.append([[2, 0], [2, 1], [2, 2], [2, 3]])
        self._field_positions.append([[-2,-4],[7,0]])
        self._lowest_col_position.append([[-2,-4],[7,0]])

        # self._rotations.append([[0, 2], [1, 2], [2, 2], [3, 2]])
        # self._rotations.append([[1, 0], [1, 1], [1, 2], [1, 3]])


class JPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.type = "J"
        # rotations ordered by their rotation to the right
        self._rotations.append([[0, 0], [0, 1], [1, 1], [2, 1]])
        self._field_positions.append([[0,-2],[7,0]])
        self._lowest_col_position.append([[0,-2],[9,0]])

        self._rotations.append([[1, 0], [2, 0], [1, 1], [1, 2]])
        self._field_positions.append([[-1,-3],[7,0]])
        self._lowest_col_position.append([[-1,-3],[8,0]])

        self._rotations.append([[0, 1], [1, 1], [2, 1], [2, 2]])
        self._field_positions.append([[0,-3],[7,-1]])
        self._lowest_col_position.append([[0,-3],[7,-1]])

        self._rotations.append([[1, 0], [1, 1], [0, 2], [1, 2]])
        self._field_positions.append([[0,-3],[8,0]])
        self._lowest_col_position.append([[0,-3],[9,0]])


class SPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.type = "S"
        # rotations ordered by their rotation to the right
        self._rotations.append([[1, 0], [2, 0], [0, 1], [1, 1]])
        self._field_positions.append([[0,-2],[7,0]])
        self._lowest_col_position.append([[0,-1],[8,0]])

        self._rotations.append([[1, 0], [1, 1], [2, 1], [2, 2]])
        self._field_positions.append([[-1,-3],[7,0]])
        self._lowest_col_position.append([[-1,-3],[7,0]])

        # self._rotations.append([[1, 1], [2, 1], [0, 2], [1, 2]])
        # self._rotations.append([[0, 0], [0, 1], [1, 1], [1, 2]])


class TPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.type = "T"
        # rotations ordered by their rotation to the right
        self._rotations.append([[1, 0], [0, 1], [1, 1], [2, 1]])
        self._field_positions.append([[0,-2],[7,0]])
        self._lowest_col_position.append([[0,-2],[7,0]])

        self._rotations.append([[1, 0], [1, 1], [2, 1], [1, 2]])
        self._field_positions.append([[-1,-3],[7,0]])
        self._lowest_col_position.append([[-1,-3],[8,0]])

        self._rotations.append([[0, 1], [1, 1], [2, 1], [1, 2]])
        self._field_positions.append([[0,-3],[7,-1]])
        self._lowest_col_position.append([[0,-3],[8,-1]])

        self._rotations.append([[1, 0], [0, 1], [1, 1], [1, 2]])
        self._field_positions.append([[0,-3],[8,0]])
        self._lowest_col_position.append([[0,-3],[8,0]])


class ZPiece(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.type = "Z"
        self._rotations.append([[0, 0], [1, 0], [1, 1], [2, 1]])
        self._field_positions.append([[0,-2],[7,0]])
        self._lowest_col_position.append([[0,-2],[8,0]])

        self._rotations.append([[2, 0], [1, 1], [2, 1], [1, 2]])
        self._field_positions.append([[-1,-3],[7,0]])
        self._lowest_col_position.append([[-1,-2],[8,0]])

        # self._rotations.append([[0, 1], [1, 1], [1, 2], [2, 2]])
        # self._rotations.append([[1, 0], [0, 1], [1, 1], [0, 2]])
