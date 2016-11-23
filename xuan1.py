# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:10:43 2016

@author: auk13
"""

import numpy as np
import pprint
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# INIT =====================================================================================

n = 101

sq = np.zeros((n, n))

sq[50][50] = 1

"Note: the array is padded with tens to form a boundary which avoids out of range errors in the next neighbour function below"
"This seems to be the quickest method for now. Tried throwing exceptions for nearest boundary values but it has to check for each point so is slower"

"Further optimisation can be done on removing redundant squares so they don't have to be looped over"

sq = np.insert(sq, n, values=2, axis=1)  # right side of array
sq = np.insert(sq, 0, values=2, axis=1)  # left side of array

sq = np.insert(sq, n, values=2, axis=0)  # top side of array (bottom after inverted)
sq = np.insert(sq, 0, values=2, axis=0)  # bottom side of array

# FN =======================================================================================


def eden_b_step(array):
    """
    Gets all nearest neighbour array elements, then picks one randomly and fills it

    :param array:
    :param list_var:
    :return:
    """

    list_var = []

    for i in range(1, len(array)-1):
        for j in range(1, len(array)-1):
            if array[i][j] == 1:
                if array[i][j+1] == 0:
                    list_var.append([i, j+1])
                if array[i][j-1] == 0:
                    list_var.append([i, j-1])
                if array[i+1][j] == 0:
                    list_var.append([i+1, j])
                if array[i-1][j] == 0:
                    list_var.append([i-1, j])
    print list_var

    __t = tuple(random.choice(list_var))  # convert to tuple so it can be used as array coordinate values
    print __t
    sq[__t] = 1

for i in range(2000):
    eden_b_step(sq)

plot = plt.imshow(sq, cmap='hot')
plt.gca().invert_yaxis()
pprint.pprint(sq)
plt.show()

