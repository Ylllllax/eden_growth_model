import numpy as np
import pprint
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# INIT =====================================================================================

l = []

n = 11
sq = [[0 for k in xrange(n)] for j in xrange(n)]

sq[5][5] = 1

# FN =======================================================================================

def neighbour(array, list):
    """
    Gets nearest neighbour array elements

    :param array:
    :param list:
    :return:
    """

    for i in range(len(array)):
        for j in range(len(array)):
            if array[i][j] == 1:
                if array[i+1][j+1] == 0:
                    list.append([i+1, j+1])
                if array[i+1][j-1] == 0:
                    list.append([i+1, j-1])
                if array[i-1][j+1] == 0:
                    list.append([i-1, j+1])
                if array[i-1][j-1] == 0:
                    list.append([i-1, j-1])

                print list

neighbour(sq, l)
pprint.pprint(sq)

plot = plt.imshow(sq, cmap='hot')
plt.gca().invert_yaxis()
plt.show()
