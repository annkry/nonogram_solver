'''The algorithm for solving a nonogram will consist of first randomly selecting whether it will be a column or a row, then I will randomly select 
the corresponding column or row number. I will use dynamic programming, where dp[i][j] will represent the minimum number of bit swaps required so that 
the blocks from 0 to i are placed no further than position j. This will allow me to determine which field will have its value changed from 0 to 1 or 
from 1 to 0. 

0 will represent a white field - unpainted, and 
1 will represent a black field - painted. 

The program will keep the current image in the tab array. 
Additionally, I will search for the minimum number of bit changes in the sequence for more than one possible block.'''

from cmath import inf
import random


def opt(list, blocks):
    n = len(list)
    m = len(blocks)
    suma = sum(blocks)
    dp = [[-1] * n for i in range(m)]
    pref = [-1] * n
    pref[0] = list[0]
    prefb = [-1]*m
    prefb[0] = blocks[0]
    for j in range(1, m):
        prefb[j] = prefb[j-1]+blocks[j]
    for j in range(1, n):
        pref[j] = pref[j-1]+list[j]

    dp[0][blocks[0]-1] = blocks[0]-(pref[blocks[0]-1])
    for j in range(blocks[0], n):
        dp[0][j] = min(blocks[0]-(pref[j]-pref[j-blocks[0]]) +
                       (pref[j-blocks[0]]), dp[0][j-1]+list[j])

    for i in range(1, m):
        j = sum(blocks[0:i+1])-1+i
        dp[i][j] = blocks[i]-(pref[j]-pref[j-blocks[i]]) + \
            list[j-blocks[i]]+dp[i-1][j-blocks[i]-1]
        j = j+1
        if i != m-1:
            end = n-(suma-prefb[i])-(m-i)
        else:
            end = n-1
        for k in range(j, end+1):
            if k-blocks[i]-1 < 0:
                dp[i][k] = min(blocks[i]-(pref[k]-pref[k-blocks[i]]) +
                               list[k-blocks[i]], dp[i][k-1]+list[k])
            else:
                dp[i][k] = min(blocks[i]-(pref[k]-pref[k-blocks[i]]) + dp[i-1]
                               [k-blocks[i]-1] + list[k-blocks[i]], dp[i][k-1]+list[k])
    return dp[m-1][n-1]


def finish(a, b, k, w):
    for c in range(0, a):
        if w[c] != 0:
            return False
    for d in range(0, b):
        if k[d] != 0:
            return False
    return True


def print_state(tab, a, b):
    for q in range(0, a):
        for g in range(0, b):
            if tab[q][g] == 1:
                print('#', end='')
            else:
                print('.', end='')
        print('')


def min_change_col(tab, a, j, c):
    list = []
    for h in range(0, a):
        list.append(tab[h][c])
    return opt(list, j[c])


def min_change_row(tab, i, r):
    return opt(tab[r], i[r])


file = open('zad_input.txt')
p = 0
a = 0
b = 0
i = []
j = []
for linia in file:
    list_from_file = linia.split()
    num = [int(s) for s in list_from_file if s.isdigit()]
    if p == 0:
        a = num[0]
        b = num[1]
    elif p <= a:
        i.append(num)
    else:
        j.append(num)
    p += 1

tab = []  # 0 - white fields, 1 - black fields

tab = [[0] * b for i in range(a)]
list = []
improvement = 0
gl = 0

w = []  # matching rows
for r in range(0, a):
    w.append(min_change_row(tab, i, r))
k = []  # matching rows
for r in range(0, b):
    k.append(min_change_col(tab, a, j, r))


while not finish(a, b, k, w):
    if gl > 4000:
        w = []  # matching rows
        for r in range(0, a):
            w.append(min_change_row(tab, i, r))
        k = []  # matching columns
        for r in range(0, b):
            k.append(min_change_col(tab, a, j, r))
        tab.clear()
        tab = [[0] * b for i in range(a)]
        improvement = 0
        gl = 0
        list.clear()
    else:
        r1 = random.randint(0, a-1)  # row is fixed, we will look for y
        r2 = random.randint(0, b-1)  # fixed column, we are looking for x
        w_lub_k = random.randint(0, 1)
        if w_lub_k == 0:
            # row is fixed, we will look for y
            id_x = r1
            id_y = 0
            max = -3
            id_y_min = 0
            min_row = 0
            min_col = 0
            listmax = []
            for g in range(0, b):
                id_y = g
                tab[id_x][id_y] = 1-tab[id_x][id_y]
                new_k = min_change_col(tab, a, j, id_y)
                new_w = min_change_row(tab, i, id_x)
                # we want new_k+new_w to be the smallest, i.e. we want improvement to be the largest
                improvement = w[id_x] + k[id_y] - (new_k + new_w)
                tab[id_x][id_y] = 1-tab[id_x][id_y]
                if max <= improvement and improvement != -2:
                    if improvement > max:
                        listmax.clear()
                        max = improvement
                    listmax.append(g)
                    min_row = new_w
                    min_col = new_k
            if max != -3:
                id_y_min = listmax[random.randint(0, len(listmax)-1)]
                tab[id_x][id_y_min] = 1-tab[id_x][id_y_min]
                w[id_x] = min_change_row(tab, i, id_x)
                k[id_y_min] = min_change_col(tab, a, j, id_y_min)
        else:  # fixed column, we are looking for x
            id_x = 0
            id_y = r2
            max = -3
            id_x_min = 0
            min_row = 0
            min_col = 0
            listmax = []
            for g in range(0, a):
                id_x = g
                tab[id_x][id_y] = 1-tab[id_x][id_y]
                new_k = min_change_col(tab, a, j, id_y)
                new_w = min_change_row(tab, i, id_x)
                improvement = w[id_x] + k[id_y] - (new_k + new_w)
                tab[id_x][id_y] = 1-tab[id_x][id_y]
                if max <= improvement and improvement != -2:
                    if improvement > max:
                        listmax.clear()
                        max = improvement
                    listmax.append(g)
                    min_row = new_w
                    min_col = new_k
            if max != -3:
                id_x_min = listmax[random.randint(0, len(listmax)-1)]
                tab[id_x_min][id_y] = 1-tab[id_x_min][id_y]
                w[id_x_min] = min_change_row(tab, i, id_x_min)
                k[id_y] = min_change_col(tab, a, j, id_y)
        gl += 1

# saving the result to an output file
file = open("zad_output.txt", "w")
for q in range(0, a):
    for g in range(0, b):
        if tab[q][g] == 1:
            print('#', end='', file=file)
        else:
            print('.', end='', file=file)
    print('', file=file)

file.close()
