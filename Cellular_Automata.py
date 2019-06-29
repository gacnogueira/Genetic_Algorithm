from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors
from random import randint
from matplotlib import colors
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
import os
import time
pp = PdfPages('multipage.pdf')
def ternary (n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))

def generate_lattice(ls, k):
    lattice = []
    for x in range(ls) :
        if(k==2):
            lattice.append(str(randint(0, 1)))
        else:
            lattice.append(str(randint(0, 2)))
    return lattice

def condition_generator(r, phi, k):
    n = r * 2 + 1
    number_conditions = k**n
    if(k == 2):
        phi = bin(phi)[2:].zfill(number_conditions)
    else:
        phi = ternary(phi).zfill(number_conditions)
    phi = phi[::-1]
    return phi

def update_lattice(lattice, phi, r) :
    NextL = []
    
    for x in range(len(lattice)) : #para cada elemento da lattice
        left = ""
        right = ""
        for y in range(r, 0, -1) :
            pos_left, pos_right = x - y, (x + (r - y) + 1) % len(lattice)
            
            left += str(lattice[pos_left])
            right += str(lattice[pos_right])
        neighbourhood = int(left + str(lattice[x]) + right, 2)
        NextL.append(phi[neighbourhood])
    return(NextL)

def run_ca(lattice, phi, r) :
    matrix = []
    matrix.append(lattice)
    new_lattice = []
    new_lattice = lattice
    #elapsed_time_updatelattice = []
    for y in range(180):
        #start_time_updatelattice = time.time()
        matrix.append(update_lattice(new_lattice, phi, r))
        new_lattice = matrix[-1]
        #elapsed_time_updatelattice.append(time.time() - start_time_updatelattice)
    #print('Time for running update_lattice: ', sum(elapsed_time_updatelattice)/180, ' Total time of update lattices: ', sum(elapsed_time_updatelattice))
    return matrix

def plot_and_save_ca(spacetime, k) :
    if(k == 2):
        img_color = colors.ListedColormap(['white', 'black'])
    else:
        img_color = colors.ListedColormap(['white', 'black', 'yellow'])
    #SAVE TO FILE

    print("...PLOTING...")
    plt.imshow(spacetime, interpolation='nearest', cmap=img_color)
    plt.colorbar()
    plt.show()
    
    print("...SAVING TO MATRIX_PLOT.pdf...")
    spacetime = np.array(spacetime)
    plt.imsave('MATRIX_PLOT.pdf',spacetime, cmap=img_color)
    print("...SUCCESSFULLY SAVED...")
    
    
    
    
def inputs():
    ls = 100 
    tm = 200
    phi = int(input("phi?\n"), 10)
    r = int(input("Insert Radius\n"))
    k = int(input("Insert K\n"))
    return ls, tm, phi, r, k

def CA():
    #print(new_rules)
    
    
    ls, tm, phi, r, k = inputs()
    lattice = generate_lattice(ls, k)
    Y = []
    x = []
    
    phi = condition_generator(r, phi, k)
    x = run_ca(lattice, phi, r)
    Y.append(x)
    mat_in_int = []
    m = len(Y)
    w = len(x[0])
    h = len(x)
    print('X: ', x)
    mat_in_int = [[0]*w] * h 
    matrixes = [mat_in_int] * m
    i = 0
    
    for row in range(len(x)):
    #print("ROW NUMBER:", row)
        new_row = []
        for col in range(len(x[row])):

            #print("COL NUMBER:", col, "ELEMENT=",x[row][col])
            new_row.append(int(x[row][col]))
            continue
        #print(mat_in_int[row], x[row])
        mat_in_int[row] = new_row
       

    
    
    plot_and_save_ca(mat_in_int, k)
    
    

    
'''
rules:
 para base 16:
phi = 0504058605000F77037755877BFFB77F
r=3
k=2
 para base 10
phi = 18
r = 1
k = 2
'''