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
import threading


def initialize_pool(k, ls, nt):
    T, Temp_T = [], []
    for x in range(nt):
        Temp_T = CA.generate_lattice(ls, k)
        while Temp_T in T:
            Temp_T = CA.generate_lattice(ls, k)
        T.append(Temp_T)
    return T
#print(initialize_pool(2, 100, 100))

def initialize_population(r, k, np):
    P = []
    n = k * 2 + 1
    number_possible_rules = k ** k ** n
    for x in range(np):
        rule = CA.condition_generator(r, randint(0, number_possible_rules), k)
        if rule not in P:
            P.append(rule)
    
    return P
#print(initialize_population(1, 2, 50))

def score_synchronization(matrix_espaco_tempo):
    fourthtolast_lattice, thirdtolast_lattice, secondtolast_lattice, last_lattice = matrix_espaco_tempo[-4], matrix_espaco_tempo[-3], matrix_espaco_tempo[-2], matrix_espaco_tempo[-1]
    one, zero = '1', '0'
    
        
    ones = fourthtolast_lattice.count('1')
    zeros = len(fourthtolast_lattice) - ones
        
    if ones > zeros:
        C = ones + thirdtolast_lattice.count(zero) +secondtolast_lattice.count(one) + last_lattice.count(zero)
    else:
        C = zeros + thirdtolast_lattice.count(one) +secondtolast_lattice.count(zero) + last_lattice.count(one)
    return float(C/(4*len(last_lattice)))
    
def fitness_synchronization(phi, T, r):
    temp_score = 0
    scores = []
    average_score = 0
    for lattice in T:
        temp_matrix = CA.run_ca(lattice, phi, r)
        temp_score = score_synchronization(temp_matrix)
        scores.append(temp_score)
    average_score = sum(scores)/len(T)
    print('average_score: ', average_score)
    return average_score
#print(fitness_synchronization('011101000', initialize_pool(2, 101, 100), 1))
        
def crossover(parent1, parent2, points):
    if(points == 1):
        pos = int(randint(1, len(parent1)))
        return parent1[:pos]+parent2[pos:], parent2[:pos]+parent1[pos:]
    elif(points == 2):
        pos = int(randint(1, int(len(parent1)/2)))
        pos2 = int(randint(pos, len(parent1)))
        return parent1[:pos]+parent2[pos:pos2]+parent1[pos2:], parent2[:pos]+parent1[pos:pos2]+parent2[pos2:]
#print(crossover([1,2,3,4,5,6,7,8,9], [9,8,7,6,5,4,3,2,1], 2))

def mutate(phi, m):
    for c in phi:
        if random.random() < m:
            c = randint(0,1)
    return phi

def run_generation(P, T, e, r, k, points, m):
    rules_P = defaultdict(list)
    next_generation, offspring_temp = [], []
    
    for phi in P:
        rules_P[phi] = fitness_synchronization(phi, T, r)
    
    rules_P = [i[0] for i in sorted(rules_P.items(), 
                                    key=lambda x: x[1], 
                                    reverse=True)]
    for rule in range(e):
        next_generation.append(rules_P[rule])
    i = 0
    turns = (len(P) - e)
    while i < turns/2:
        offspring_temp += crossover(next_generation[randint(0, e-1)], 
                                    next_generation[randint(0, e-1)], 
                                    points)
        i += 1
    for offs in offspring_temp :
        offs = mutate(offs, m)
    next_generation += (offspring_temp)
    print('next_generation: ', next_generation)
    
    return [next_generation]

def run_GA(r, k, e, np, nt, points, tm, m, ls):
    P = initialize_population(r, k, np)
    rules = []
   
    for y in range(tm):
        print('Generation ', y+1)
        T = initialize_pool(k, ls, nt)
        rules = run_generation(P, T, e, r, k, points, m)
        P.clear()
        P = rules[-1]

    
    

    new_rules = []
    for rule in new_rules:
        new_rules.append(int(rule[::-1],2))
    
    print('new_rules', new_rules)
    with open('output_rules.txt', 'wb') as f:
        npy.savetxt(f, new_rules, fmt='%s')

    
    
    #CA.CA(ls, tm, new_rules, r, k)
    

    
    print(rules)

run_GA(3, 2, 5, 15, 20, 2, 20, 0.03, 100)
'''
ls = 100
r = 3
k = 2

rules = [1977960021, 1977971143, 1969571413, 1028354503, 1977971285, 1977971285, 1977960021, 1977971143, 1969571413, 1977971143, 1977960021, 1977971143, 1977971285, 1969582677, 1977960021]
CA.CA(ls, rules, r, k)
'''