import numpy as npy
import matplotlib.pyplot as plt
from matplotlib import colors
from random import randint
import random
import Cellular_Automata as CA
import re
from collections import Counter
from collections import defaultdict
import operator
from matplotlib.backends.backend_pdf import PdfPages
import time

maximum_rules = []
header = [['Generation', 'Rule', 'fitness']]


def initialize_pool(k, ls, nt):
    T, Temp_T = [], []
    for x in range(nt):
        Temp_T = CA.generate_lattice(ls, k)
        while Temp_T in T:
            Temp_T = CA.generate_lattice(ls, k)
        T.append(Temp_T)
    return T


def initialize_population(r, k, np):
    P = []
    n = k * 2 + 1
    number_possible_rules = k ** k ** n
    for x in range(np):
        rule = CA.condition_generator(r, randint(0, number_possible_rules), k)
        if rule not in P:
            P.append(rule)

    return P


def score_synchronization(matrix_espaco_tempo):
    fourthtolast_lattice, thirdtolast_lattice, secondtolast_lattice, last_lattice = matrix_espaco_tempo[-4], \
                                                                                    matrix_espaco_tempo[-3], \
                                                                                    matrix_espaco_tempo[-2], \
                                                                                    matrix_espaco_tempo[-1]
    one, zero = '1', '0'
    if fourthtolast_lattice.count(one) == secondtolast_lattice.count(one) and thirdtolast_lattice.count(
            zero) == last_lattice.count(zero):
        if fourthtolast_lattice.count(one) > fourthtolast_lattice.count(zero):
            C = secondtolast_lattice.count(one) + last_lattice.count(zero)
        else:
            C = secondtolast_lattice.count(zero) + last_lattice.count(one)
    else:
        return 0
    return float(C / (2 * len(last_lattice)))


def fitness_synchronization(phi, T, r):
    temp_score = 0
    scores = []
    average_score = 0
    for lattice in T:
        temp_matrix = CA.run_ca(lattice, phi, r)
        temp_score = score_synchronization(temp_matrix)
        scores.append(temp_score)
    average_score = sum(scores) / len(T)
    return average_score


def crossover(parent1, parent2, points):
    if (points == 1):
        pos = int(randint(2, len(parent1) - 2))
        return [parent1[:pos] + parent2[pos:], parent2[:pos] + parent1[pos:]]
    elif (points == 2):
        pos = int(randint(8, 16))
        pos2 = int(randint(pos, 27))
        return [parent1[:pos] + parent1[pos:pos2] + parent2[pos2:],
                parent1[:pos] + parent2[pos:pos2] + parent1[pos2:],
                parent1[:pos] + parent2[pos:pos2] + parent2[pos2:],
                parent2[:pos] + parent1[pos:pos2] + parent1[pos2:],
                parent2[:pos] + parent1[pos:pos2] + parent2[pos2:],
                parent2[:pos] + parent2[pos:pos2] + parent1[pos2:]]


def mutate(phi, m):
    for c in phi:
        if random.random() < m:
            if c == 0:
                c = 1
            else:
                c = 0
    return phi


def run_generation(P, T, e, r, k, points, m, tm, i):
    initial_time = time.time()
    rules_P = defaultdict(list)
    next_generation, offspring_temp = [], []
    for phi in P:
        rules_P[phi] = fitness_synchronization(phi, T, r)
    rules = [i[0] for i in sorted(rules_P.items(),
                                  key=lambda x: x[1],
                                  reverse=True)]
    fitnesses = [i[1] for i in sorted(rules_P.items(),
                                      key=lambda x: x[1],
                                      reverse=True)]
    row = []
    for x in range(len(rules)):
        row = (i, rules[x], fitnesses[x])
        header.append(row)
    if (i == tm):
        for rule in range(len(P) - 1):
            next_generation.append(rules[rule])
        return next_generation
    for rule in range(e):
        next_generation.append(rules[rule])
    t = 0
    turns = (len(P) - e)
    while len(offspring_temp) < len(P) - e:
        # t = 0
        parent1 = next_generation[randint(0, e - 1)]
        parent2 = next_generation[randint(0, e - 1)]
        while parent1 == parent2:
            parent2 = next_generation[randint(0, e - 1)]
        print('(', i, ')', 'parent1: ', parent1, ' parent2: ', parent2)

        ofssp = crossover(parent1, parent2, points)

        # print('(',i,')','parent1: ', parent1,' parent2: ', parent2)
        # u = 0
        for off in ofssp:
            off = mutate(off, m)
            if off not in offspring_temp and off not in next_generation:
                offspring_temp.append(off)
                print('(', i, ')', off, 'entrou no offspring')
            else:
                print('(', i, ')', off, 'Não entrou no offspring')
            # u += 1

        overP = len(offspring_temp) - (len(P) - e)
        if overP > 0:
            while len(offspring_temp) > turns:
                offspring_temp.pop()

    next_generation += (offspring_temp)
    print('Time for generation ', i, ': ', (time.time() - initial_time) / 60)
    return [next_generation]


def run_GA(r, k, e, np, nt, points, tm, m, ls):
    P = initialize_population(r, k, np)
    rules = []
    i = 1
    percentage = 0
    for y in range(tm):
        if int(y * 100 / tm) > percentage:
            percentage = int(y * 100 / tm)
            print(percentage, "%")
        T = initialize_pool(k, ls, nt)
        print('Generation: ', i)
        rules = run_generation(P, T, e, r, k, points, m, tm, i)
        P.clear()
        P = rules[-1]
        i += 1
    print(maximum_rules)
    npy.savetxt("Regras.csv", header, '%s', delimiter=",")


run_GA(3, 2, 20, 50, 100, 2, 120, 0.04, 100)
