import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import datetime

class BallisticDeposition:
    
    def __init__(self, L_x):
        
        """need to enter parameters as floats; actual system width is L_x-2 as edge columns are not used;
        Insert True if you want to impose periodic boundary conditions"""
        self.__xsize = L_x
     
        m = 0
        n = 0
        self.__total_particles=m #keeps track of how many times the instance has been propagated       
        if isinstance(L_x, int) == True:
            system_array = np.zeros((1, self.__xsize)) #indices go from 0 to self.__xsize-1
            self.__system_array = system_array 
        else:
            raise Exception("need to insert an integer")
            
        
    def __repr__(self):
        return "%s(number of columns = %g)" % ("system size", self.__xsize)
        
    
    def __str__(self):
        return "[%s]" % (self.__xsize)
        
    def number_of_deposited_particles(self):
        """returns the number of deposited particles"""
        return self.__total_particles
        
    def set_number_of_particles(self, n):
        """sets the total number of particles"""
        self.__total_particles=n 
        return self.__total_particles
    
    def system_size(self):
        """returns the system size"""
        return self.__xsize
    
    def current_array(self):
        """returns current heights"""
        return self.__system_array
        
    def random_columns(self, n): #where n is the number of iterations; function generates random column numbers
        """selects a column at random"""
        #ONLY METHOD THAT CHANGES WHEN IMPOSING PERIODIC BOUNDARY CONDITIONS
        self.chosen_columns=np.random.random_integers(0,self.__xsize-1, n) #inclusive of upper and lower bounds
        return self.chosen_columns 
    
    def array_search(self, j):
        """returns the height for a particular column"""
        return self.__system_array[0][j]
    
            
    def update_array(self, h, j): #turns a site from 0 to 1 in a matrix
        """changes the height to h for element j in the heights array"""
        self.__system_array.itemset((0,j),h)
        return self.__system_array
 
    def deposit_particles(self, n):#here n is for the number of particles we are depositing on the lattice
        """deposit n particles"""
        self.set_number_of_particles(self.number_of_deposited_particles()+n)
        self.random_columns(n) #every time is called get a DIFFERENT set of random numbers
        for j in self.chosen_columns:#if statements applying boundary conditions
            #also will work when BCs not imposed if edge columns are NEVER selected, i.e. system is effectively two columns smaller
            if j==0:
                p=self.array_search(0)+1 
                q=self.array_search(1)
                r=self.array_search(self.__xsize-1)
                
            if j==self.__xsize-1:
                p=self.array_search(self.__xsize-1)+1 
                q=self.array_search(0)
                r=self.array_search(self.__xsize-2)               
                
            else:
                p=self.array_search(j)+1 
                q=self.array_search(j+1)
                r=self.array_search(j-1)
            
            x=[p,q,r]
            h=max(x)            
            self.update_array(h, j)
        return h
        
        
    def roughness(self): #works out the roughness for a particular square matrix
        """returns the rougheness for the current heights array"""
        x=np.array([])
        
        for j in np.arange(0, self.__xsize,1):
            x=np.append(x, self.array_search(j))
            
           
        y=np.average(x)
        a=(x-y)**2  
        b=np.sum(a)
        z=(1/(float(self.__xsize)))*b #remember edge columns are kept empty so column does not
        w=z**0.5
        return w
        
    #def correlation(self):# needs working on
    #    """computes the correlation length (incomplete method)"""
    #    
    #    x=np.average(self.system_array)
    #    y=np.array([])
    #    
    #    for i in np.arange(0, self.__xsize): 
    #        for j in np.arange(0, self.__xsize):
    #        
    #            y=np.append(y, self.system_array[0][i]*self.system_array[0][j])
    #    print y.size
    #    z=(np.sum(y))/(float(self.__xsize)**2)
    #    self.correlation_length = z - x**2
    #    
    #    return self.correlation_length
               
            
    def reset_system(self, system_size=None):
        """resets system back to initial conditions with column heights of 0; the initially defined parameters remain unchanged"""
        self.__total_particles=0
        if system_size != None:
            self.__xsize = system_size
        self.__system_array= np.zeros((1, self.__xsize))    
        

    
