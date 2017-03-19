import numpy as np
import os

system_paths = ["H:\Year 4\MSci Project\Computing\Data\Eden Model C Strip Geo\systemsize100",
                "H:\Year 4\MSci Project\Computing\Data\Eden Model C Strip Geo\systemsize250",
                "H:\Year 4\MSci Project\Computing\Data\Eden Model C Strip Geo\systemsize500",
                "H:\Year 4\MSci Project\Computing\Data\Eden Model C Strip Geo\systemsize1000"] #directories for each system size 

file_paths_100 =  os.listdir(system_paths[0])
file_paths_250 = os.listdir(system_paths[1])
file_paths_500 = os.listdir(system_paths[2])
file_paths_1000 = os.listdir(system_paths[3]) #corresponds to above, change according to no. of directories
file_paths_list = [file_paths_100, file_paths_250, file_paths_500, file_paths_1000]
roughness_array_list = [100,250,500,1000] #just a series of lists with length = no. of directories (values arbitrary)
time_array_list = [100,250, 500, 1000]
upper_error_bars_list = [100, 250, 500, 1000]
lower_error_bars_list = [100, 250, 500, 1000]
data_points_list = [100, 250, 500, 1000]

def sort_roughness(system_index, data_points): #system index [100,250,500,1000] = (0,1,2,3); data points for each simulation
    i=0
    for file in file_paths_list[system_index]:
        f = open(os.path.abspath(
            os.path.join(system_paths[system_index],
                         file)))
        for line in f:
            i = i + len(line.split()) #returns no of. simulations
            break
    print i # i is the number of simulations, i.e. total number of columns of all test files in specified directory (i.e. specific system size)
    roughness_array_list[system_index] = np.zeros((data_points, i)) #array to store all data

    m=0 #counter for the column index
    for p in np.arange(0,len(file_paths_list[system_index]),1): #cycles through all the text files for a fixed system size
        f=open(os.path.abspath(
            os.path.join(system_paths[system_index],
                         (file_paths_list[system_index])[p]))) #opens each file in turn
        #print "p=", p , "length=", len(file_paths_list[system_index])
        n = 0  # counter for the row index
        for line in f:
            if n == data_points: #only collects 10 data points
                break
            else:
                simulations = len(line.split())
                for k in np.arange(0, simulations, 1): #ensuring data points from multiple simulations within same file are also extracted
                    #print "system_index=", system_index
                    #print "simulations=", simulations
                    (roughness_array_list[system_index])[n][m+k-1]=np.exp(float(line.split()[k])) #because input data is in log form, conv to exp to get assym. error bars
                n=n+1
        m =m+simulations
    return i

def create_time_points(system_index, data_points): #assumes time also in text files
    time_list = []
    f = open(os.path.abspath(
        os.path.join(system_paths[system_index], (file_paths_list[system_index])[0])))
    n=0
    for line in f:

        if n == data_points:
            break
        else:
            time_list.append(line.split()[0])
            n = n + 1
    time_array_list[system_index] = time_list







def analyse_data(system_index, data_points, simulations): #system index [100,250,500,1000] = (0,1,2,3); data points for each simulation, simulations no indicates no. of columns
    upper_error_bars_list[system_index] = []
    lower_error_bars_list[system_index] =[]
    data_points_list[system_index] = []
    for n in np.arange(0,data_points,1):
        data_points = np.array([])
        for m in np.arange(0,simulations,1):
            data_points = np.append(data_points, ((roughness_array_list[system_index])[n][m]))
        standard_dev = np.std(data_points)
        average = np.mean(data_points)
        upper_bar = average + standard_dev
        lower_bar = average - standard_dev
        log_average = np.log(average)
        log_upper = np.log(upper_bar) - log_average
        log_lower = log_average - np.log(lower_bar)
        upper_error_bars_list[system_index].append(log_upper)
        lower_error_bars_list[system_index].append(log_lower)
        data_points_list[system_index].append(log_average)




def upper(system_index):
    for i in upper_error_bars_list[system_index]:
        print i

def lower(system_index):
    for i in lower_error_bars_list[system_index]:
        print i

def average(system_index):
    for i in data_points_list[system_index]:
        print i

def time(system_index):
    for i in time_array_list[system_index]:
        print i
#now create arrays of raw data
a = sort_roughness(0,10) #system size 100 10 data points for each simulation
b = sort_roughness(1,11) #system size 250 11 data points
c = sort_roughness(2,11) #system size 500 11 data points
d = sort_roughness(3,12) #system size 1000

#create_time_points(0, 10)
#create_time_points(1, 11)
#create_time_points(2, 11)
#create_time_points(3, 12)

#create arrays of averages and upper/lower error bars; access using upper(), lower() and average() funcs
analyse_data(0,10,a) #creat
analyse_data(1,11,b)
analyse_data(2,11,c)
analyse_data(3,12,d)