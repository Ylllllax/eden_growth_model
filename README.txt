To run the code, you need to have the following files in your directory:

- BallisticStripGeo.py (contains class for BD)
- EdenABCStripGeo.py   (contains classes for Eden A, B and C)
- DataAnalysis.py      (contains Data Analysis class)


Open the DataAnalysis.py file and run it
- the BD and Eden classes are all imported on running the file

Create an instance of a BD or Eden class and then collect data using an instance of the Data Analysis class and the log_log_origin() method
belonging to the DataAnalysis class

For sample scroll further down

-----------------------------------------------------------------------------------------------------------

Model classes are instantiated using

- BallisticDeposition(system size) 
- EdenAsystem(system size)
- EdenBsystem(system size)
- EdenCsystem(system size)

Data Analysis class is instantiated using

- DataAnalysis()

The DataAnalysis has a method log_log_origin(self, other, initial_power, data_points, simulations, system_sizes)

This takes the model class instance and propagates the system, depositing particles and calculating the roughness at logarithmic intervals,
yielding a chosen number of data points stored in a text file.

other = Instantiation of system to be analysed
initial_power = first data point represents 2**(initial power) deposited particles
data_points = number of data points; log log scale 
simulations = number of simulations per system; yields average data points and assocciated error bars
system_sizes = number of different system sizes simulated; starts with system size of model class instance and each successive system size is larger by 500

------------------------------------------------------------------------------------------

Sample Code

b=DataAnalysis()
a=EdenCsystem(1000)
b.log_log_origin(a, 4, 15, 10, 4)

