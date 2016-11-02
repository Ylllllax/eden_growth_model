#animation file
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ballisticdepositionbothBCandnoBC import BallisticDeposition 

fig = plt.figure(1)
a= BallisticDeposition(100.,100., True)
im = plt.imshow(a.matrix, cmap='hot')

def update_figure(i):# i is the number of iterations
    
        a.fill_matrix(20)
        
        im.set_array(a.matrix)
                  
        return plt.imshow(a.matrix, cmap='hot')

ani = animation.FuncAnimation(fig, update_figure, frames=1, interval=5)                   
plt.show()
