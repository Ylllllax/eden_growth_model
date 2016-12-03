# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:10:43 2016

@author: auk13
"""

import numpy as np
import pprint
import random
import matplotlib.pyplot as plt
import time
import matplotlib.image as mpimg

# INIT =====================================================================================

n = 101

sq = np.zeros((n, n))

#sq[50][50] = 1
print sq
"Note: the array is padded with tens to form a boundary which avoids out of range errors in the next neighbour function below"
"This seems to be the quickest method for now. Tried throwing exceptions for nearest boundary values but it has to check for each point so is slower"

"Further optimisation can be done on removing redundant squares so they don't have to be looped over"
sq[0,:]=1
sq = np.insert(sq, n, values=2, axis=1)  # right side of array
sq = np.insert(sq, 0, values=2, axis=1)  # left side of array

sq = np.insert(sq, n, values=2, axis=0)  # top side of array (bottom after inverted)
sq = np.insert(sq, 0, values=2, axis=0)  # bottom side of array

# FN =======================================================================================


def eden_step(array, x, steps):
    """
    Gets all nearest neighbour array elements, then picks one randomly and fills it

    :param array:
    :param x: determines if want Eden A, B, or C. 0 = A, 1 = B, 2 = C
    :param steps: how many steps to iterate
    :return:
    """
#    list_neighbours = []
    list_surface = []

    "Adds all starting cells to the possible cells to grow list. Note: this will only work properly if the seed is a line or a single seed - square/disk will not work due to extra" \
        "stuff in the middle"

    for i2 in range(0, len(array)):
        for j in range(0, len(array)):
            if array[i2][j] == 1:
                list_surface.append([i2, j]) #stores initial seed or strip coordinates

    for i in range(steps):
        list_neighbours = []
        "Fill the nearest neighbour list from list_surface"

        for x in range(0, len(list_surface)):
            
            # Turn element into tuple so we can use it for array
            tuplex = tuple(list_surface[x])
            # Unpack the tuple
            i, j = tuplex
            if array[i][j+1] == 0:
                list_neighbours.append([i, j+1])
            if array[i][j-1] == 0:
                list_neighbours.append([i, j-1])
            if array[i+1][j] == 0:
                list_neighbours.append([i+1, j])
            if array[i-1][j] == 0:
                list_neighbours.append([i-1, j])
#        print list_neighbours    #(gives you a list of all the neighbours)

        __t = tuple(random.choice(list_neighbours))  # convert to tuple so it can be used as array coordinate values; picking a random neighbour and then decide whether it can be occupied
    #    print __t
#        sq[__t] = 1

        "Now do code for adding the new element to surface if it satisfies conditions."

        i, j = __t
        temp_list = []
        if array[i][j + 1] == 0:
            list_surface.append([i, j])
            sq[i,j] = 1
        elif array[i][j - 1] == 0:
            list_surface.append([i, j])
            sq[i,j] = 1
        elif array[i + 1][j] == 0:
            list_surface.append([i, j])
            sq[i,j] = 1
        elif array[i - 1][j] == 0:
            list_surface.append([i, j]) #i.e. if it has at least one unoccupied neighbour then it lies on the surface
            sq[i,j] = 1
            "now looking at neighbouring sites to chosen unoccupied neighbour"
        if array[i][j + 1] == 1:
            temp_list.append([i, j+1])
        if array[i][j - 1] == 1:
            temp_list.append([i, j-1])
        if array[i + 1][j] == 1:
            temp_list.append([i+1, j])
        if array[i - 1][j] == 1:
            temp_list.append([i-1, j])

        "Also check existing cells if full and remove them from list_surface if needed."

        for x in range(0, len(temp_list)):
            i, j = temp_list[x]
            checker = 0
            if array[i][j + 1] != 0:
                checker += 1
            if array[i][j - 1] != 0:
                checker += 1
            if array[i + 1][j] != 0:
                checker += 1
            if array[i - 1][j] != 0:
                checker += 1

            if checker == 4:
                if temp_list[x] in list_surface:
                    sq[i,j]=2
                    list_surface.remove(temp_list[x])


"RUNNING AND TIMING"

start = time.time()

eden_step(sq, 1, 100)

end = time.time()
print (end - start)  # execution time in seconds. Put this before the plot, because otherwise it will time the time until you close the graph window

"END RUNNING AND TIMING"

plot = plt.imshow(sq, cmap='hot')
plt.gca().invert_yaxis()
pprint.pprint(sq)
plt.show()
