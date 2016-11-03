import numpy as np
import pprint
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# INIT =====================================================================================

n = 11

sq = np.zeros((n, n))

sq[10][5] = 1

"Note: the array is padded with tens to form a boundary which avoids out of range errors in the next neighbour function below"

sq = np.insert(sq, n, values=10, axis=1)
sq = np.insert(sq, 0, values=10, axis=1)

sq = np.insert(sq, n, values=10, axis=0)
sq = np.insert(sq, 0, values=10, axis=0)

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
                    list_var.append([i+1, j+1])
                if array[i][j-1] == 0:
                    list_var.append([i+1, j-1])
                if array[i+1][j] == 0:
                    list_var.append([i-1, j+1])
                if array[i-1][j] == 0:
                    list_var.append([i-1, j-1])
    print list_var

    __t = tuple(random.choice(list_var)) #convert list to tuple

""""This doesn't work yet: I need to change the tuple into coordinates such that the function can get the coordinates in the array sq. Then I just change that value of sq to 1 to fill up and complete the Eden B step"""

    print list_var[__t[0], __t[1]]


eden_b_step(sq)

plot = plt.imshow(sq, cmap='hot')
# plt.gca().invert_yaxis()
plt.show()

pprint.pprint(sq)
