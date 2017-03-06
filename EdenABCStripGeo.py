import numpy as np
import pprint
import random
import matplotlib.pyplot as plt
import time
import matplotlib.image as mpimg
import datetime
import itertools
from operator import itemgetter, attrgetter, methodcaller

class Common(object):
    """provides namespace for methods shared by Eden classes"""
    
    def __init__(self, system_size):
        """defines the system size, all constituent row arrays objects will be of this size"""       
        self.__system_size=system_size
        self.__array_list=[]
        seed=np.zeros((1,system_size))  #initial line of seeds denoted by 1
        empty=np.zeros((1,system_size))
        for i in np.arange(0,system_size):
            seed[0][i]=1
        self.__array_list.append(seed)
        self.__array_list.append(seed) #adds the second array describing the line of seeds to the array_list (two seed layer ensures the interface grows in the correct direction!)
        self.__array_list.append(empty) #initial layer of unoccupied sites 
        self.__list_surface_sites=[]
        for i in np.arange(0,system_size,1):
            self.__list_surface_sites.append([1,i]) #storing coordinates in format [row_index, column_index]
    
    def system_size(self):
        """returns system size"""
        return self.__system_size
        
    def array_list(self):
        """returns the complete list of arrays representing each row from oldest to newest"""
        return self.__array_list

    def delete_row(self,row_number):
        """deletes row from the list of arrays of system data"""
        self.__array_list.remove(self.__array_list[row_number])
        
    def dogroupby(self, k, sorted=sorted, groupby=itertools.groupby, list=list):
        """deletes duplicates elements in list; function needed for Eden A"""
        ks = sorted(k)
        return [i for i, _ in itertools.groupby(ks)]
        
    def surface_sites(self):
        """returns list of surface site coordinates"""
        return self.__list_surface_sites
        
    def add_surface_site(self, i, j):
        """adds the coordinates of a site to the list of surface sites"""
        self.__list_surface_sites.append([i,j])
        
    def remove_surface_site(self, i, j):
        """searches for and removes the site with the specified coordinates from the list"""
        x = len(self.__list_surface_sites)
        for a in np.arange(0,x,1):
            b=self.surface_sites()
            c=b[a]
            if c[0] == i and c[1] == j:
                self.__list_surface_sites.remove([i,j])
                break
        return self.__list_surface_sites     
            
    def add_empty_row(self):
        """adds an empty row to the list of system arrays; the array is the same size as all the other array (defined by the system size)"""
        self.__array_list.append(np.zeros((1,self.__system_size)))
        
    def update_array_list(self, i, j, value):
        """changes a specified element in the system list of arrays to a chosen value"""
        (self.__array_list[i])[0][j] = value
        
    def return_element(self, i, j):
        """returns the value of a specific element from the system list of arrays"""
        return (self.__array_list[i])[0][j]
        
    def nearest_neighbours(self, i, j):
        """identifies the values of the four nearest neighbours, also returning the coordinates in form [i,j]"""
        w=(i+1)%len(self.__array_list) #modulo division takes care of periodic boundary conditions
        x=(j+1)%(self.__system_size)
        y=(i-1)%len(self.__array_list)
        z=(j-1)%(self.__system_size)
        i_mod=i%len(self.__array_list)
        j_mod=j%(self.__system_size)
        a=self.return_element(w,j_mod)
        b=self.return_element(i_mod,x)
        c=self.return_element(y,j_mod)
        d=self.return_element(i_mod,z)
        
        return [[w,j_mod],a], [[i_mod,x],b], [[y,j_mod],c], [[i_mod,z],d]    
   
    def add_site(self, i, j):
        """adds a site and removes sites that are no longer on the surface from the surface sites list"""
        self.update_array_list(i, j, 1) #occupies the chosen site in the list of arrays
        right, up, left, down = self.nearest_neighbours(i,j)
        
        if right[1] == 0:          #adding new site to list of surface sites if it has at least one unoccupied neighbour
            self.add_surface_site(i,j)   
        elif up[1] == 0:
            self.add_surface_site(i,j) 
        elif left[1] == 0:
            self.add_surface_site(i,j)     
        elif down[1] == 0:
            self.add_surface_site(i,j)  
            
        x=(i+1)%len(self.__array_list)    
        y=j
        right, up, left, down = self.nearest_neighbours(x,y)
        if right[1] != 0 and up[1] != 0 and left[1] != 0 and down[1] != 0:
            self.remove_surface_site(x,y)    
        x=i
        y=(j+1)%(self.__system_size)
        right, up, left, down = self.nearest_neighbours(x,y)
        if right[1] != 0 and up[1] != 0 and left[1] != 0 and down[1] != 0:
            self.remove_surface_site(x,y)    
        x=(i-1)%len(self.__array_list)
        y=j
        right, up, left, down = self.nearest_neighbours(x,y)
        if right[1] != 0 and up[1] != 0 and left[1] != 0 and down[1] != 0:
            self.remove_surface_site(x,y)    
        x=i
        y=(j-1)%(self.__system_size)
        right, up, left, down = self.nearest_neighbours(x,y)
        if right[1] != 0 and up[1] != 0 and left[1] != 0 and down[1] != 0:
            self.remove_surface_site(x,y)
    
    def to_add_or_not_to_add(self):
        """works out if another empty list needs to be added to the array, so the system can expand"""
        a=len(self.__array_list)-1
        b=(self.__array_list)[a]
        m=0 #counter
        for i in np.arange(0,self.__system_size,1):
            if b[0][i] == 0:
                m=m+1
        if m != self.__system_size:
            self.add_empty_row()
    
    def delete_bulk(self): 
        """deletes data for the bulk which is not needed"""
        a=self.__list_surface_sites
        row_indices_list=[]
        
        for i in np.arange(0,len(self.__list_surface_sites)):
            row_indices_list.append((a[i])[0])
        b=min(row_indices_list)
        
        if b-2 >= 0:
            m=0
            while m < b-1:
                self.delete_row(0)
                m=m+1
            for i in np.arange(0,len(self.surface_sites()),1):
                (self.__list_surface_sites[i])[0]=(self.__list_surface_sites[i])[0]-m                   

                                            
    def deposit_particles(self, iterations):
        """execute the simulation for a specified number of particles"""        
        m=0
        #start = np.datetime64(datetime.datetime.now())
        while m <= iterations:
            self.to_add_or_not_to_add()
            x, y =tuple(self.random_neighbour())
            self.add_site(x,y)
            self.delete_bulk()
            m=m+1
        #end = np.datetime64(datetime.datetime.now())
        #print start, end
        
        
    def matrix_representation(self):
        """writes all the data from the list of arrays into a matrix of the required size; enables visualisation"""
        self.__matrix = np.zeros((len(self.__array_list),self.__system_size))
        for i in np.arange(0,len(self.__array_list),1):
            for j in np.arange(0,self.__system_size,1):
                self.__matrix[i][j] = (self.__array_list[i])[0][j]  #copying data into a separate matrix so it can be represented visually
        for i in np.arange(0,len(self.surface_sites()),1): #adjust colour of surface sites to see if correct sites are stored in code
            x, y = tuple((self.surface_sites())[i])
            self.__matrix[x][y] = 2
        return self.__matrix     
        
    
    def visual_representation(self):
        """plots imshow colour map for system"""
        fig = plt.figure()
        im = plt.imshow(self.matrix_representation(), cmap='Blues')  
        return plt.show()
    
    def roughness(self):# ---------------------------------> next step to define a roughness, best way to do this using list of surface sites
        """returns the roughness of the Eden system""" 
        x=np.array([])
        temp_list=[]
        a=self.surface_sites()
        b=sorted(a, key=itemgetter(1)) 
        m=0 #counter used in for loop
        for i in np.arange(0,len(b), 1):
            if (b[i])[1] == m: # i.e. is the surface site part of the SAME column
               temp_list.append((b[i])[0]) # append the height, i.e. row index
            else: # i.e. moving on to NEXT column
                m=m+1 # updating current column index
                x=np.append(x, max(temp_list)) # append max height in column
                temp_list=[]
                temp_list.append((b[i])[0])
        x=np.append(x, max(temp_list)) # to deal with last column
        y=np.average(x)
        a=(x-y)**2  
        b=np.sum(a)
        z=(1/(float(self.system_size())))*b #remember edge columns are kept empty so column does not
        w=z**0.5
        return w

    def reset_system(self, system_size=None):
        """resets system back to initial conditions with column heights of 0; the initially defined parameters remain unchanged"""
        print self.__system_size
        if system_size != None:
            self.__system_size=system_size
        self.__array_list=[]
        seed=np.zeros((1,system_size))  #initial line of seeds denoted by 1
        empty=np.zeros((1,system_size))
        for i in np.arange(0,system_size):
            seed[0][i]=1
        self.__array_list.append(seed)
        self.__array_list.append(seed) #adds the second array describing the line of seeds to the array_list (two seed layer ensures the interface grows in the correct direction!)
        self.__array_list.append(empty) #initial layer of unoccupied sites 
        self.__list_surface_sites=[]
        for i in np.arange(0,system_size,1):
            self.__list_surface_sites.append([1,i]) #storing coordinates in format [row_index, column_index]
        
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~COMMON FUNCTIONS TO EDEN MODELS ABOVE; UNIQUE FUNCTIONS BELOW~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##########################################################################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~              
                            
class EdenAsystem(Common):
    """has attributes of the Eden A model"""
    
    def __init__(self, system_size):
         Common.__init__(self, system_size)    
    
#~~~~~~~~~~~~~~~~UNIQUE METHODS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def identify_neighbours(self):
        """identifies neighbours of the surface sites which could be occupied at the next time step"""
        self.__unoccupied_neighbours=[]
        
        for a in self.surface_sites():
            i,j = tuple(a)  
            right, up, left, down = self.nearest_neighbours(i,j) 
            
            if right[1] == 0:
               self.__unoccupied_neighbours.append(right[0])   
            if up[1] == 0:
                self.__unoccupied_neighbours.append(up[0])
            if left[1] == 0:
                self.__unoccupied_neighbours.append(left[0])    
            if down[1] == 0:
                self.__unoccupied_neighbours.append(down[0])      
        self.__unoccupied_neighbours=self.dogroupby(self.__unoccupied_neighbours, sorted=sorted, groupby=itertools.groupby, list=list) #extra line in this function compared to Eden B; deletes duplicates (also requires extra groupby function)
        return self.__unoccupied_neighbours    

    def random_neighbour(self):
        """using the identify_neighbours() func to pick a single neighbour site at random"""
        a=self.identify_neighbours()
        b=np.random.randint(0,len(a),1)
        return a[b]



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###############################################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        

class EdenBsystem(Common):
    """has attributes of the Eden B model"""

    def __init__(self, system_size):
         Common.__init__(self, system_size)    
                                                      
#~~~~~~~~~~~~~~~~~~~~~~~~~UNIQUE METHODS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
           
    def identify_neighbours(self):
        """identifies neighbours of the surface sites which could be occupied at the next time step"""
        self.__unoccupied_neighbours=[]
        
        for a in self.surface_sites():
            i,j = tuple(a)  
            right, up, left, down = self.nearest_neighbours(i,j) 
            
            if right[1] == 0:          #modulo division imposes periodic boundary conditions
               self.__unoccupied_neighbours.append(right[0])   
            if up[1] == 0:
                self.__unoccupied_neighbours.append(up[0])
            if left[1] == 0:
                self.__unoccupied_neighbours.append(left[0])    
            if down[1] == 0:
                self.__unoccupied_neighbours.append(down[0])
        return self.__unoccupied_neighbours
    
    def random_neighbour(self):
        """using the identify_neighbours() func to pick a single neighbour site at random"""
        a=self.identify_neighbours()
        b=np.random.randint(0,len(a),1)
        return a[b]
    

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
##########################################################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    
class EdenCsystem(Common):
    """has attributes of the Eden C model"""
    
    def __init__(self, system_size):
         Common.__init__(self, system_size)         
                                                
        
#~~~~~~~~~~~~~~~~~~~~~~~~~UNIQUE METHODS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    def random_neighbour(self):
        """function that picks surface site at random and subsequently picks an 
        empty neighbour at random; replaces functionality of random_neighbour(self) and 
        identify_neighbours() used in Eden A and B"""
        a=len(self.surface_sites())
        b=np.random.randint(0,a,1)
        m=0 #counter for number of unoccupied neighbouring sites
        i=(self.surface_sites()[b])[0]
        j=(self.surface_sites()[b])[1]
        right, up, left, down = self.nearest_neighbours(i,j)
        unoccupied_nearest_neighbours=[]
        if right[1] == 0:   #counting number of surrounding unoccupied sites
               m=m+1
               unoccupied_nearest_neighbours.append(right[0])   
        if up[1] == 0:
                m=m+1
                unoccupied_nearest_neighbours.append(up[0])  
        if left[1] == 0:
                m=m+1
                unoccupied_nearest_neighbours.append(left[0])      
        if down[1] == 0:
                m=m+1
                unoccupied_nearest_neighbours.append(down[0])  
        c=np.random.randint(0,m,1)
        return unoccupied_nearest_neighbours[c] #returns at random one of the unoccupied nearest neighbours of a randomn surface site (i.e. Eden C)    


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################################################################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    

