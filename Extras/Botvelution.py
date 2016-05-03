# -*- coding: utf-8 -*-
# Python3.4*
from numpy import random
import subprocess
import sys
import time
from heapq import heappop, heappush, nlargest
from random import choice
import pickle

'''
 This is a genetic algorithm for learning feature weights of my agent. It produces an initial population of 100
 randomly defined feature weights for my bot. Then randomly selects pairs from the population and has them play
 a game of tetris against eachother, fitness is based off the length of the game. After all couples have participated
 in a game a new generation is created by keeping the top 10 preformers of the last generation, and then selecting
 90 more couples (selected via triangular distribution where beter preforming couples are more likely to reproduce).
 After producing 90 offspring, the children are go through an unlikely chance of mutation, then the new population is tested
 again and the proces repeats.
'''

class Botvelution:
    def __init__(self, num_features):
        self.num_features = num_features
        self.best_couple = None

        self.pop = None


    def run(self):

        print("0. Initializing the population")
        self.initialize_population(100)

        # run for 10,000 generations
        for x in range(10000):
            print("\n----GENERATION "+ str(x)+"----\n")

            print("1. Testing Population")
            couples = self.test_population()

            tot_rounds = 0.0
            for couple in couples:
                tot_rounds += couple[0]
            print("  average rounds survived: "+str(tot_rounds/len(couples))+'\n')

            print("2. Getting New Generation")
            self.get_next_generation(couples)

            print("3. Best individuals")
            pickle.dump( self.best_couples, open( "best_params.p", "wb" ) )
            for couple_idx in range(len(self.best_couples)):
                score = self.best_couples[couple_idx][0]
                couple = self.best_couples[couple_idx][1]

                print("  "+str(couple_idx+1)+") SCORE: "+str(score)+"\n     "+str(couple[0])+"\n     "+str(couple[1]))

            print("4. Repeat\n\n")

    def get_next_generation(self, couples):
        sorted_couples = sorted(couples, reverse=True)

        self.best_couples = sorted_couples[:5]

        new_pop = []
        parents_to_keep = 0

        for i in range(parents_to_keep):
            new_pop.append(sorted_couples[i][1][0])
            new_pop.append(sorted_couples[i][1][1])


        for j in range(len(couples)-parents_to_keep):
            idx = int(random.triangular(0,0,len(couples)))
            parent_1 = sorted_couples[idx][1][0]
            parent_2 = sorted_couples[idx][1][1]


            child_1, child_2 = self.mate(parent_1,parent_2)

            self.mutate(child_1)
            self.mutate(child_2)

            new_pop.append(child_1)
            new_pop.append(child_2)


        self.pop = new_pop

    def mutate(self,c):
        for feat_idx in range(len(c)):
            if choice(range(101)) > 98:
                c[feat_idx] = random.random_sample()*10 - 5


    def mate(self, p1, p2):

        if choice(range(10)) < 8:
            place = choice(range(len(p1)))
        else:
            return p1, p2
        return p1[:place] + p2[place:], p2[:place] + p1[place:]


    def test_population(self):
        couples = []

        order = random.permutation(len(self.pop))
        first_half = order[:int(len(self.pop)/2)]
        second_half = order[int(len(self.pop)/2):]

        for idx in range(int(len(self.pop)/2)):
            final_round = 0

            command = open("run.sh", 'w')

            parent_1 = self.pop[first_half[idx]]
            parent_2 = self.pop[second_half[idx]]

            print(" COUPLE: "+str(idx))
            print("  parent 1: "+str(parent_1))
            print("  parent 2: "+str(parent_2))

            call = '#!/bin/bash\n\njava -cp bin com.theaigames.blockbattle.Blockbattle "python3 /Users/Computer/Desktop/Block-Engine/Block-Bots/CT-Bot/BotRun.py height_weight='+str(parent_1[0])+' line_weight='+str(parent_1[1])+' holes_weight='+str(parent_1[2])+' bumpiness_weight='+str(parent_1[3])+' valleys_weight='+str(parent_1[4])+'" "python3 /Users/Computer/Desktop/Block-Engine/Block-Bots/CT-Bot/BotRun.py height_weight='+str(parent_2[0])+' line_weight='+str(parent_2[1])+' holes_weight='+str(parent_2[2])+' bumpiness_weight='+str(parent_2[3])+' valleys_weight='+str(parent_2[4])+'" 2>err.txt 1>out.txt'

            command.write(call)
            command.close()


            subprocess.call('./run.sh', shell=False)

            output = open("out.txt", 'r')
            line = output.readline()
            count = 0
            while line[:5] != 'stopp':
                final_round = line[line.rfind(' ')+1:]

                line = output.readline()

                if count > 100:
                    break
                count += 1

            output.close()

            couples.append((int(final_round),[parent_1,parent_2]))

            print("  rounds survived: "+str(final_round))


        return couples

    def initialize_population(self, size):
        pop = []
        for _ in range(size):
            feats = []
            for _ in range(self.num_features):
                feats.append(random.random_sample()*10 - 5)
            pop.append(feats)

        self.pop = pop

if __name__ == '__main__':
    num_features = 5
    Botvelution(num_features).run()
