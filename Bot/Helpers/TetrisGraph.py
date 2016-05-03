# -*- coding: utf-8 -*-
# Python3.4*

'''
 This is a primitive graph structure used to traverse up the tetris board and "escape" the currently falling piece.
 Movements start at the possible drop location of the piece, and work backwards to the initial position of the piece.
 Some bottom locations are impossible to reach and therefore cannot be escaped. In this case the escape function returns
 None instead of a list of moves.
'''
class Graph:
    def __init__(self, des_pos, des_rot, init_pos, init_rot, f, p):
        self.piece = p
        self.desired_pos = des_pos
        self.desired_rot = des_rot
        self.initial_pos = init_pos
        self.initial_rot = init_rot

        self.field = f

    def escape(self):
        moves = None

        # creat the initial node where the drop locaton of the piece is projected
        n = Node(self.initial_pos, self.initial_rot, [], None)

        # initialize a count (if 50 moves are made then assume the drop position is impossible to reach and try another position)
        count = 0
        # while there are nodes with actions left to try
        while n is not None:
            # get the "best" action to do next
            action = n.get_best_action(self.desired_pos, self.desired_rot)

            # if there is no action returned this node is "dead", therefore back track and find a new path
            if not action:
                n = n.prev_node
                continue
            # otherwise, make the action
            else:
                n = n.make_action(action, self.piece, self.field)

            # if the action puts the piece in the correct position and rotation: the correct escape moves were found, therefore break
            if n.pos[0] == self.desired_pos[0] and n.pos[1] == self.desired_pos[1]+1 and n.rot == self.desired_rot:
                moves = n.moves
                break

            # if the position has gone through 50 tries break and try a new position (aka assume the position is impossible to reach)
            if count == 50:
                moves = None
                break
            count += 1

        # returns a list of moves, or None if the drop position is impossible to reach
        return moves

'''
 Each node in the graph has six possible movements and will try them all before "dying" and therefore not being traversed to again.
 This is a Best First Search, choosing the best possible action via a greedy hueristic of which action brings the piece closest
 to the desired position.
'''
class Node:
    def __init__(self, pos, rot, moves, last_node):
        self.actions = ["down","turnLeft","turnRight","left","right","up"]
        self.tried_actions = []

        self.pos = pos
        self.rot = rot

        self.prev_node = last_node

        self.moves = moves

    def make_action(self, action_str, piece, field):
        # initialize the offset of the action
        pos = [0,0]
        rot = 0

        # get the x,y,r offset of the action string
        action = self.action_to_xyr(action_str)

        # apply the offset to the piece positions
        pos[0] = self.pos[0] + action[0]
        pos[1] = self.pos[1] + action[1]
        rot = self.rot - action[2]

        # rotations must also be completed on the piece itself
        if action_str == "turnRight":
            piece.turnRight(times=1)
        if action_str == "turnLeft":
            piece.turnLeft(times=1)

        # project the piece in the new offset location, this will either return a valid field or None if the location is invalid
        test_field = field.projectPiece(piece,pos)

        # by default return the same node (because the action was a failure we need to try another)
        n = self

        # if the action produces a valid field append the move to the move list and return the newly traversed to node
        if test_field:
            moves = self.moves
            server_action = self.escape_action_to_server_action(action_str)
            moves = [server_action] + moves

            n = Node(pos, rot, moves, self)
        # otherwise, if the node is dead return the node that it was traversed to from
        elif self.is_dead():
            n = self.last_node

        return n

    '''
     Ranks actions based of how much they minimize the distance of the piece's current position to the desired position.
     XY distance is calculated using Euclidean Distance, Rotaions distance is based off the absolute difference in the piece's
     current and desired rotaion index
    '''
    def get_best_action(self, desired_pos, desired_rot):
        x_diff = self.pos[0] - desired_pos[0]
        y_diff = self.pos[1] - desired_pos[1]+1

        xy_dist = (x_diff**2 + y_diff**2)**0.5
        r_dist = abs(self.rot - desired_rot)

        best_dist = 2*xy_dist + r_dist
        best_action = None
        pos = [0,0]
        for action_str in self.actions:

            if action_str not in self.tried_actions:
                action = self.action_to_xyr(action_str)

                pos[0] = self.pos[0] + action[0]
                pos[1] = self.pos[1] + action[1]
                rot = self.rot - action[2]

                x_diff = pos[0] - desired_pos[0]
                y_diff = pos[1] - desired_pos[1]

                xy_dist = (x_diff**2 + y_diff**2)**0.5
                r_dist = abs(rot - desired_rot)

                new_dist = xy_dist + r_dist

                if new_dist < best_dist:
                    best_dist = new_dist
                    best_action = action_str


        self.tried_actions.append(best_action)
        return best_action

    '''
     If a node has no more actions to complete it is dead
    '''
    def is_dead(self):
        return len(self.actions) == 0

    '''
     Converts the action string into a [x,y,r] array defining the action's effects on piece position and rotation
    '''
    def action_to_xyr(self, action):
        switcher = {
            "up": [0,-1,0],
            "right": [1,0,0],
            "left": [-1,0,0],
            "turnright": [0,0,-1],
            "turnleft": [0,0,1],
            "down": [0,1,0]
        }

        return switcher.get(action.lower())

    '''
     Converts the graph action string (defining a piece traversing up the board)
     into a valid server move (defining a piece falling down the board)
    '''
    def escape_action_to_server_action(self, action):
        switcher = {
            "up": "down",
            "right": "left",
            "left": "right",
            "turnright": "turnleft",
            "turnleft": "turnright",
            "down": "up"
        }

        return switcher.get(action.lower())
