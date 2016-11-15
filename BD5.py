import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

class BallisticDeposition:
    """store all heights as a 1 dim array"""
    
    def __init__(self, L_x, Periodic_BCs=None):
        
        """need to enter parameters as floats; actual system width is L_x-2 as edge columns are not used;
        Insert True if you want to impose periodic boundary conditions"""
        self.__xsize = L_x
        self.__Periodic_BCs=Periodic_BCs
        m = 0
        n = 0
        self.propagation_number=m #keeps track of how many times the instance has been propagated
        self.total_particles=n
        roughness_array=np.array([])
        self.roughness_array=roughness_array #empty array used for roughness values 
        time_array=np.array([])
        self.time_array=time_array   #empty array used for corresponding time values
        
        if isinstance(L_x, int) == True:
            system_array = np.zeros((1, self.__xsize)) #indices go from 0 to self.__xsize-1
            self.system_array = system_array 
        else:
            raise Exception("need to insert an integer")
            
        
    def __repr__(self):
        return "%s(number of columns = %g)" % ("system size", self.__xsize)
        
    
    def __str__(self):
        return "[%s]" % (self.__xsize)
    
    def size_of_system(self):
        return self.__xsize
    
    def current_array(self):
        return self.system_array
        
    def random_columns(self, n): #where n is the number of iterations; function generates random column numbers
        #ONLY METHOD THAT CHANGES WHEN IMPOSING PERIODIC BOUNDARY CONDITIONS
        if self.__Periodic_BCs == True:
            self.chosen_columns=np.random.random_integers(0,self.__xsize-1, n) #inclusive of upper and lower bounds
            
        else:
            self.chosen_columns=np.random.random_integers(1,self.__xsize-2, n) #inclusive of upper and lower bounds
        
        return self.chosen_columns 
    
    def array_search(self, j):
        """returns the height for a particular column"""
        
        return self.system_array[0][j]
    
            
    def update_array(self, h, j): #turns a site from 0 to 1 in a matrix
        
        self.system_array.itemset((0,j),h)
        return self.system_array
 
    def deposit_particles(self, n):#here n is for the number of particles we are depositing on the lattice
        
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
            #print j, self.system_array
         
        return h
        
        
    def roughness(self): #works out the roughness for a particular square matrix
        """returns the rougheness for the array"""
        x=np.array([])
        
        for j in np.arange(0, self.__xsize,1):
            x=np.append(x, self.array_search(j))
            
           
        y=np.average(x)
        a=(x-y)**2  
        b=np.sum(a)
        z=(1/(float(self.__xsize)))*b #remember edge columns are kept empty so column does not
        w=z**0.5
        return w
        
        
    def roughness_dynamics(self, n, iterations):#generates a series of roughness values for a series of matrices
        """iterates the BD forward in time, depositing n particles for each of the iterations; takes instance of the BallisticDeposition class"""
        self.n=n                   #property of the data analysis object
        self.iterations=iterations #property of the dataanalysis object
        
        self.propagation_number= self.propagation_number + self.iterations   #property of the BallisticDeposition object; total no. of iterations ,i.e. data values
        self.total_particles = self.total_particles + self.iterations*self.n #property of the BallisticDeposition object; total no. of particles deposited
        x=np.array([])
        m=1
        while m<=iterations:
            self.deposit_particles(n)           
            x=np.append(x, self.roughness())
            m = m+1
            print m-1
        self.data=x
        
        return self.data
        
    def add_data(self):
        """filling data into separate roughness array and creating the matching time array; need to enter numpy array as the parameter"""

        for i in np.arange(0, self.data.size):
            self.roughness_array=np.append(self.roughness_array, self.data[i])
        self.time_array=np.append(self.time_array, np.arange(self.total_particles-(self.iterations-1)*self.n, self.total_particles+self.n,self.n))
                
        return self.roughness_array, self.time_array
    
    def erase_data(self):
        self.roughness_array=np.array([])
        self.time_array=np.array([])
        return self.roughness_array, self.time_array
        
    def partial_erase_data(self, first_index, last_index):
        """erases all the elements in between and including those given by the indices"""
        self.roughness_array=np.delete(self.roughness_array, np.arange(first_index, last_index+1))
        self.time_array=np.delete(self.time_array, np.arange(first_index, last_index+1))
        return self.roughness_array, self.time_array
    
    def line_plot(self, line_of_best_fit=None):

        log_t=np.log(self.time_array)
        log_w=np.log(self.roughness_array)
        m, b = np.polyfit(log_t, log_w, 1)
        
        fig = plt.figure()
        fig.suptitle('Log-log Plot of Roughness Against Time', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        ax.set_title('axes title')

        ax.set_xlabel('log(t)')
        ax.set_ylabel('log(w)')
        ax.plot(log_t, log_w, 'r+')
        if line_of_best_fit == True:
            
            ax.plot(log_t, m*log_t + b, '-')
            ax.text(0.1,0.9, r'$\beta=$%g' % (m) , style='italic', horizontalalignment='left',verticalalignment='top', transform=ax.transAxes ) 
        ax.text(0.1,0.8, 'Particles Deposited=%g'  % (self.total_particles)  , style='italic', horizontalalignment='left',verticalalignment='top', transform=ax.transAxes ) #position of test and the test itself
        #plt.axis([40, 160, 0, 0.03])
        plt.grid(True)
        plt.show()
        
        return None
    
    def saturation_value(self): 
        
        w_sat = np.average(self.roughness_array)
    
    
         
         
         
         
         
        
    

        
        
        
    
            
        