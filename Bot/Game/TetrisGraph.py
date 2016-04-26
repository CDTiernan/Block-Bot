# -*- coding: utf-8 -*-
# Python3.4*


class Graph:
    def __init__(self, des_pos, des_rot, init_pos, init_rot, f, p):
        #self.log = open("graphOut.txt", 'w')

        self.desired_pos = des_pos
        self.desired_rot = des_rot
        self.initial_pos = init_pos
        self.initial_rot = init_rot

        self.field = f
        self.piece = p


        #self.log.write("Graph Output:\n\n")
        #self.log.close()

        #self.Nodes = [[None]*field.width]*field.height



    def escape(self):
        #self.log = open("graphOut.txt", 'a')
        moves = None

        n = Node(self.initial_pos, self.initial_rot, [], None)

        #self.log.write(self.field.toString(self.field.projectPiece(self.piece,[self.desired_pos[0],self.desired_pos[1]])))


        count = 0
        while n is not None:

            action = n.get_best_action(self.desired_pos, self.desired_rot)
            #self.log.write(str(action)+"\n\n")
            if not action:
                n = n.prev_node
                continue
            else:
                n = n.make_action(action, self.piece, self.field)


            #self.log.write(str(n.pos)+"\n")
            #self.log.write(str(n.rot)+"\n")
            #self.log.write(str(self.desired_pos)+"\n")
            #self.log.write(str(self.desired_rot)+"\n")
            if n.pos[0] == self.desired_pos[0] and n.pos[1] == self.desired_pos[1]+1 and n.rot == self.desired_rot:
                #self.log.write('escaped+\n')
                #self.log.write(self.field.toString(self.field.projectPiece(self.piece,[n.pos[0],n.pos[1]])))
                moves = n.moves
                break

            if count == 50:
                #self.log.write('skipping')
                moves = None
                break
            count += 1

        #self.log.close()

        return moves


class Node:
    def __init__(self, pos, rot, moves, last_node):
        #self.node_log = open("nodeOut.txt", 'w')

        self.actions = ["down","turnLeft","turnRight","left","right","up"]
        self.tried_actions = []
        self.pos = pos
        self.rot = rot
        self.prev_node = last_node
        self.moves = moves

        #self.node_log.write("Node Output:\n\n")
        #self.node_log.close()

    def make_action(self, action_str, piece, field):
        #self.node_log = open("nodeOut.txt", 'a')

        found = False

        pos = [0,0]
        rot = 0

        action = self.action_to_xyr(action_str)
        pos = [0,0]

        pos[0] = self.pos[0] + action[0]
        pos[1] = self.pos[1] + action[1]
        rot = self.rot - action[2]

        if action_str == "turnRight":
            piece.turnRight(times=1)
        if action_str == "turnLeft":
            piece.turnLeft(times=1)

        test_field = field.projectPiece(piece,pos)

        if test_field:
            #self.node_log.write(field.toString(test_field)+"\n")
            found = True

        n = self
        if found:
            moves = self.moves
            #self.node_log.write(str(moves))
            server_action = self.escape_action_to_server_action(action_str)
            moves = [server_action] + moves

            n = Node(pos, rot, moves, self)
        elif self.is_dead():
            n = self.last_node

        #self.node_log.close()
        return n

    def get_best_action(self, desired_pos, desired_rot):
        #self.node_log = open("nodeOut.txt", 'a')
        # self.node_log.write('1')
        x_diff = self.pos[0] - desired_pos[0]
        y_diff = self.pos[1] - desired_pos[1]+1

        xy_dist = (x_diff**2 + y_diff**2)**0.5
        r_dist = abs(self.rot - desired_rot)
        #self.node_log.write(str(desired_rot))

        best_dist = 2*xy_dist + r_dist
        best_action = None
        pos = [0,0]
        for action_str in self.actions:

            if action_str not in self.tried_actions:
                # self.node_log.write(action_str+"\n")
                action = self.action_to_xyr(action_str)
                # self.node_log.write(str(action)+"\n")
                # self.node_log.write(str(self.pos[0]))

                pos[0] = self.pos[0] + action[0]
                # self.node_log.write('3.1')
                pos[1] = self.pos[1] + action[1]
                # self.node_log.write('3.2')
                rot = self.rot - action[2]
                # self.node_log.write('4')

                x_diff = pos[0] - desired_pos[0]
                y_diff = pos[1] - desired_pos[1]
                # self.node_log.write('5')

                xy_dist = (x_diff**2 + y_diff**2)**0.5
                r_dist = abs(rot - desired_rot)

                new_dist = xy_dist + r_dist

                if new_dist < best_dist:
                    best_dist = new_dist
                    best_action = action_str

                # self.node_log.write('6')


        self.tried_actions.append(best_action)
        #self.node_log.close()

        return best_action


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

    def is_dead(self):
        return len(self.actions) == 0
