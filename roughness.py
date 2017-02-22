import numpy as np

def roughness(input_array):  # ---------------------------------> next step to define a roughness, best way to do this using list of surface sites
    """returns the roughness of the Eden system"""

    y = np.average(input_array)
    a = (input_array - y) ** 2
    b = np.sum(a)
    z = (1 / (float(len(input_array)))) * b  # remember edge columns are kept empty so column does not
    w = z ** 0.5
    return w