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
"This seems to be the quickest method for now. Tried throwing exceptions for nearest boundary values but it has to check for each point so is slower"

"Further optimisation can be done on removing redundant squares so they don't have to be looped over"

sq = np.insert(sq, n, values=10, axis=1)  # right side of array
sq = np.insert(sq, 0, values=10, axis=1)  # left side of array

sq = np.insert(sq, n, values=10, axis=0)  # top side of array (bottom after inverted)
sq = np.insert(sq, 0, values=10, axis=0)  # bottom side of array

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

    __t = random.choice(list_var) # can convert list to tuple with tuple()

    print __t

""""This doesn't work yet: I need to change the tuple into coordinates such that the function can get the coordinates in the array sq. Then I just change that value of sq to 1 to fill up and complete the Eden B step"""


eden_b_step(sq)

plot = plt.imshow(sq, cmap='hot')
# plt.gca().invert_yaxis()
plt.show()

pprint.pprint(sq)
