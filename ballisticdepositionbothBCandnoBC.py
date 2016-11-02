import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class BallisticDeposition:
    
    def __init__(self, L_x, L_y, Periodic_BCs=None):
        
        """need to enter parameters as floats; actual system width is L_x-2 as edge columns are not used;
        Insert True if you want to impose periodic boundary conditions"""
        
        self.__xsize = L_x
        self.__ysize = L_y 
        self.__Periodic_BCs=Periodic_BCs

        if isinstance(L_x, float) == True and isinstance(L_y, float):
            matrix = np.zeros((self.__ysize, self.__xsize)) #indices go from 0 to self.__ysize-1/self.__xsize-1
            self.matrix = matrix
        else:
            raise Exception("need to insert a float")
            
        
    def __repr__(self):
        return "%s(number of elements in x-direction = %g, number of elements in y direction = %g)" % ("system size", self.__xsize, self.__ysize)
        
    
    def __str__(self):
        return "[%s, %s]" % (self.__xsize, self.__ysize)
        
    
    def matrix(self):
        return self.matrix
        
    def randomcolumns(self, n): #where n is the number of iterations; function generates random column numbers
        #ONLY METHOD THAT CHANGES WHEN IMPOSING PERIODIC BOUNDARY CONDITIONS
        if self.__Periodic_BCs == True:
            self.chosen_columns=np.random.random_integers(0,self.__xsize-1, n) #inclusive of upper and lower bounds
            
        else:
            self.chosen_columns=np.random.random_integers(1,self.__xsize-2, n) #inclusive of upper and lower bounds
        
        return self.chosen_columns 
        
    def empty_list(self):#initialises the empty array  #trying to store matrices for animation
        
        self.__storage_list=[]
        return self.__storage_list
        
    def store_matrix(self, matrix): #function to store matrices
        
        self.__storage_list.append(matrix)
        return self.__storage_list
        
    def matrix_list(self):
        
        return self.__storage_list
    
    
    
    def column_search(self, j): #here j is the column number
    
        x=[]
        
        for i in np.arange(0,self.__ysize,1):
            
            if self.matrix.item((i,j))==1:
                x.append(i)
            
        if len(x) != 0:
            m=min(x)-1
        
        else:
            m=self.__ysize-1
        
        return m #the index of the lowest row that is zero
            
            
    def occupy(self, i, j): #turns a site from 0 to 1 in a matrix
        
        self.matrix.itemset((i,j),1)
        return self.matrix
        
 
    def fill_matrix(self, n):#here n is for the number of particles we are depositing on the lattice
        
        self.randomcolumns(n) #every time is called get a DIFFERENT set of random numbers
        
        for j in self.chosen_columns:#if statements applying boundary conditions
            #also will work when BCs not imposed if edge columns are NEVER selected, i.e. system is effectively two columns smaller
            if j==0:
                p=self.column_search(0) #should return the required row index
                q=self.column_search(1)+1
                r=self.column_search(self.__xsize-1)+1
                
            if j==self.__xsize-1:
                p=self.column_search(self.__xsize-1) #should return the required row index
                q=self.column_search(0)+1
                r=self.column_search(self.__xsize-2)+1                
                
            else:
                p=self.column_search(j) #should return the required row index
                q=self.column_search(j+1)+1
                r=self.column_search(j-1)+1
            
            x=[p,q,r]
            y=min(x)            
            self.occupy(y, j)
         
        return self.matrix
        
    def plot_matrix(self):
        
        fig = plt.figure()
        fig.suptitle("%s %g %s" % ("Ballistic Deposition for", self.__n*self.__iterations, "Particles"), fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        ax.imshow(self.matrix, cmap='hot')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        plt.show()
        return None


    def roughness(self): #works out the roughness for a particular square matrix
        
        x=np.array([])
        
        for j in np.arange(0, self.__xsize,1):
            x=np.append(x, self.__ysize-self.column_search(j)-1)
            
        y=np.average(x)
        a=(x-y)**2  
        b=np.sum(a)
        z=(1/(self.__xsize-2))*b #remember edge columns are kept empty so column does not
        w=z**0.5
        return w
        
    
                            
    def roughness_dynamics(self, n, iterations):#generates a series of roughness values for a series of matrices
        
        x=np.array([])
        self.__n=n
        self.__iterations=iterations
        
        
        for k in np.arange(0, iterations):
            self.fill_matrix(n)
            x=np.append(x, self.roughness())
            print k 
            
        
        self.__roughness_array=x

        return self.__roughness_array
        
    def plot_graph(self):
        
        t=np.array([])
        
        for k in np.arange(1,len(self.__roughness_array)+1,1):
                t=np.append(t, k)
        
        
        log_t=np.log(t)
        log_w=np.log(self.__roughness_array)
        m, b = np.polyfit(log_t, log_w, 1)
        
        fig = plt.figure()
        fig.suptitle('Log-log Plot of Roughness Against Time', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        #ax.set_title('axes title')

        ax.set_xlabel('log(t)')
        ax.set_ylabel('log(w)')
        ax.plot(log_t, log_w, 'r+')
        ax.plot(log_t, m*log_t + b, '-')
        ax.text(0.1,0.9, r'$\beta=$%g,  Particles Deposited=%g'  % (m, self.__n*self.__iterations)  , style='italic', horizontalalignment='left',verticalalignment='top', transform=ax.transAxes ) #position of test and the test itself
        #plt.axis([40, 160, 0, 0.03])
        plt.grid(True)
        plt.show()
        
       
        
        return None

    
    
        
        
    

        
        
        
    
            
        