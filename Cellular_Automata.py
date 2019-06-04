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
            pos_left = x - y
            pos_right = (x + (r - y) + 1) % len(lattice)
            left += str(lattice[pos_left])
            right += str(lattice[pos_right])
        neighbourhood = left + str(lattice[x]) + right
        neighbourhood = int(neighbourhood, 2)
        NextL.append(phi[neighbourhood])
    return(NextL)

def run_ca(lattice, phi, r) :
    matrix = []
    matrix.append(lattice)
    new_lattice = []
    new_lattice = lattice
    for y in range(200):
        matrix.append(update_lattice(new_lattice, phi, r))
        new_lattice = matrix[-1]
    return matrix

def plot_and_save_ca(spacetime, k, phis) :
    if(k == 2):
        img_color = colors.ListedColormap(['white', 'black'])
    else:
        img_color = colors.ListedColormap(['white', 'black', 'yellow'])
    nrows, ncols = 4, 4
    figsize = [10, 10]
    x = 0
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    rules = []
    for rule in phis:
        rules.append(rules)
    for i, axi  in enumerate(ax.flat):
        #axi.set_title("phi"+str(rule[x]))
        axi.imshow(spacetime[i], cmap=img_color)
        x += 1
        
    plt.show()
    
    
    
    '''
    
    print(spacetime)
    if(k == 2):
        img_color = colors.ListedColormap(['white', 'black'])
    else:
        img_color = colors.ListedColormap(['white', 'black', 'yellow'])
    #SAVE TO FILE
    pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
    print("...PLOTING...")
    fig = plt.imshow(spacetime, interpolation='nearest', cmap=img_color)
    fig.colorbar()
    
    
    print("...SAVING TO MATRIX_PLOT.pdf...")
    spacetime = np.array(spacetime)
    fig.imsave('MATRIX_PLOT.pdf',spacetime, cmap=img_color)
    print("...SUCCESSFULLY SAVED...")
    
    
    for fig in range(1, figure().number): ## will open an empty extra figure :(
        pdf.savefig( fig )
    
    '''
    '''
    print("...SAVING TO MATRIX_PLOT.pdf...")
    spacetime = np.array(spacetime)
    plt.savefig(pp, spacetime, cmap=img_color)
    plt.savefig()
    print("...SUCCESSFULLY SAVED...")
    pp.close
    '''
    
def inputs():
    ls = 100 
    tm = 200
    phi = int(input("phi?\n"), 10)
    r = int(input("Insert Radius\n"))
    k = int(input("Insert K\n"))
    return ls, tm, phi, r, k

def CA(ls, new_rules, r, k):
    print(new_rules)
    lattice = generate_lattice(ls, k)
    

    Y = []
    x = []
    print(new_rules)
    for rule in new_rules:
        print(rule)
        phi = condition_generator(r, rule, k)
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
    for matrix in range(len(new_rules)):
        for row in range(len(x)):
        #print("ROW NUMBER:", row)
            new_row = []
            for col in range(len(x[row])):

                #print("COL NUMBER:", col, "ELEMENT=",x[row][col])
                new_row.append(int(x[row][col]))
                continue
            #print(mat_in_int[row], x[row])
            mat_in_int[row] = new_row
        matrixes[matrix] = mat_in_int

    
    
    plot_and_save_ca(matrixes, k, new_rules)
    
    

    
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