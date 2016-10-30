import numpy as np
import pprint
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# INIT =====================================================================================

l = []

n = 11
sq = [[0 for k in xrange(n)] for j in xrange(n)]

sq[10][5] = 1

"Note: the array is padded with tens to form a boundary which avoids out of range errors in the next neighbour function below"

np.pad(sq, (1, 1), 'constant', constant_values=10)

# todo: this doesnt work yet

# FN =======================================================================================


def neighbour(array, list_var):
    """
    Gets all nearest neighbour array elements

    :param array:
    :param list_var:
    :return:
    """

    for i in range(1, len(array)-1):
        for j in range(1, len(array)-1):
            if array[i][j] == 1:
                if array[i+1][j+1] == 0:
                    list_var.append([i+1, j+1])
                if array[i+1][j-1] == 0:
                    list_var.append([i+1, j-1])
                if array[i-1][j+1] == 0:
                    list_var.append([i-1, j+1])
                if array[i-1][j-1] == 0:
                    list_var.append([i-1, j-1])

neighbour(sq, l)
pprint.pprint(sq)

plot = plt.imshow(sq, cmap='hot')
plt.gca().invert_yaxis()
plt.show()
