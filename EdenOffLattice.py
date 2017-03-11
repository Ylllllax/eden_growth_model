import scipy
import numpy as np
from scipy.optimize import fsolve
import pylab
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches
#need to insert %matplotlib qt into the command line before running the program; not for pycharm though
#need to write method that sorts the masking_range_list, so there is NO OVERLAPPING of ranges ---> is this necessary

class Disc:

    def __init__(self, number, radius, initial_x, initial_y):
        """only adjustable parameter (so far) is the radius; will be adjusted in roughness simulations"""
        self.__number=number #disc number; incremented sequentially
        self.__radius=radius #radius of disc
        self.__xcoord=initial_x #x coordinate of disc origin
        self.__ycoord=initial_y #y coordinate of disc origin
        self.__masking_angle_ranges=[] #all masking range angles are taken CLOCKWISE
        self.__masked_running_total=[] #used in calculation of random surface point
        self.__masking_status = "Not completely masked" #changes to masked when disc is masked
        self.__list_of_neighbours = [] #list of disc numbers that are considered neighbour
        self.__cross_over_points = []  #all the cross over points with other discs
        self.__uncompressed_masking_ranges = [[],[]] #used to track all masking ranges passed through this disc
        self.__list_masked_neighbours = [] #neighbours that are masked

    def __repr__(self):
        return "%s = %g %s = %g %s = %g %s = %g" % ("disc number", self.number(), "radius", self.radius(), "x", self.x_coordinate(),"y", self.y_coordinate())

    def __str__(self):
        return "%s = %g" % ("r", self.__radius)

    def number(self):
        """returns disc number in system"""
        return self.__number

    def radius(self):
        """returns radius of disc"""
        return self.__radius

    def coordinate(self):
        """returns x and y coordinate of disc origin"""
        return self.__xcoord, self.__ycoord

    def x_coordinate(self):
        """returns x coordinate of disc origin"""
        return self.__xcoord

    def y_coordinate(self):
        """returns y coordinate of disc origin"""
        return self.__ycoord

    def masking_range(self):
        """returns current masking angle ranges in radians(ranges are clockwise)"""
        return self.__masking_angle_ranges

    def null_masking_range(self):
        """removes ranges; used when masked discs are used in crossover point calculations"""
        self.__masking_angle_ranges = []

    def angle_running_total(self):
        """returns total size of unmasked angle that forms part of the surface"""
        return self.__masked_running_total

    def masking_status(self):
        """returns masking status; either "completely masked" or "not completely masked" """
        return self.__masking_status

    def cross_over_points(self):
        """returns all the crossover points calculated for this disc"""
        return self.__cross_over_points

    def uncompressed_masking_ranges(self):
        """returns all the masking angle ranges calculated for this disc without any compression"""
        return self.__uncompressed_masking_ranges

    def neighbours(self):
        """returns list of disc numbers corresponding to unmasked neighbours"""
        return self.__list_of_neighbours

    def masked_neighbours(self):
        """returns list of disc numbers corresponding to completely masked neighbours"""
        return self.__list_masked_neighbours

    def update_neighbours(self, neighbour):
        """adds new disc number as a neighbour"""
        self.__list_of_neighbours.append(neighbour)

    def delete_neighbour(self, neighbour):
        """deletes disc number from neighbour list when it is masked"""
        if neighbour in self.__list_of_neighbours:
            self.__list_of_neighbours.remove(neighbour)
        else:
            print neighbour

    def update_masked_neighbours(self, masked_neighbour):
        """adds masked neighbour to masked neighbour list"""
        self.__list_masked_neighbours.append(masked_neighbour)


    def add_crossover_points(self, cross_over_clockwise):
        """adds cross over points to the cross over points list"""
        self.__cross_over_points.append(cross_over_clockwise)

    def append_uncompressed_ranges(self, masking_range, incident_disc_number):
        """adds new masking range to the uncompressed masking range list"""
        self.__uncompressed_masking_ranges[0].append(masking_range)
        self.__uncompressed_masking_ranges[1].append(incident_disc_number)

    def add_masking_angles(self, other, masking_range):
        """takes a specified masking angle range and adds it to the masking range list
        parameter to be entered as [theta_1, theta_2], where the orientation is clockwise"""
        masking_range_two_pi = []
        element_1 = other.two_pi_limit(masking_range[0])
        element_2 = other.two_pi_limit(masking_range[1])
        masking_range_two_pi.append(element_1)
        masking_range_two_pi.append(element_2)
        self.__masking_angle_ranges.append(masking_range_two_pi)
        return self.__masking_angle_ranges

    def total_unmasked_range(self):#assume that ranges specified in masking_angle_ranges list DO NOT OVERLAP
        """returns the total unmasked angle of the disc exposed to the surface; assumes masking angle ranges are compressed"""
        running_total=2*np.pi
        for i in np.arange(0,len(self.__masking_angle_ranges),1):
            if (self.__masking_angle_ranges[i])[1]-(self.__masking_angle_ranges[i])[0] >= 0:
                running_total=running_total-((self.__masking_angle_ranges[i])[1]-(self.__masking_angle_ranges[i])[0])
                self.__masked_running_total.append(running_total)
            else:
                running_total=running_total-(2*np.pi+(self.__masking_angle_ranges[i])[1]-(self.__masking_angle_ranges[i])[0])
                self.__masked_running_total.append(running_total)
        return running_total

    def compare_two_ranges(self, range_1, range_2):
        """takes two ranges and compares them; ranges input in form range_1= [theta_1, theta_2] and range_2 = [phi_1, phi_2]
        where the orientation is clockwise and where theta_1 < phi_1"""
        theta_1 = range_1[0]
        theta_2 = range_1[1]
        phi_1 = range_2[0]
        phi_2 = range_2[1]
        if theta_2 >= theta_1:  # i.e. range_1 does not cross 2 pi mark
            if phi_2 >= phi_1:  # i.e. range_2 does not cross 2 pi mark
                if theta_2 >= phi_2:  # i.e. range_1 completely contains range_2
                    return [theta_1, theta_2]
                elif phi_2 >= theta_2 and theta_2 >= phi_1:  # i.e. range_1 and range_2 overlap
                    return [theta_1, phi_2]
                elif phi_1 >= theta_2:  # no overlap
                    return 0
            elif phi_1 >= phi_2:  # range_2 does cross 2 pi mark
                if theta_1 >= phi_2 and theta_2 >= phi_1:  # overlap
                    return [theta_1, phi_2]
                elif theta_2 >= phi_2 >= theta_1 and phi_1 >= theta_2:  # overlap
                    return [phi_1, theta_2]
                elif phi_2 >= theta_2:
                    return [phi_1, phi_2]
                elif theta_1 >= phi_2 and phi_1 >= theta_2:  # i.e. NO OVERLAP
                    return 0
                elif phi_2 >= theta_1 and theta_2 >= phi_1:  # complete masking
                    return 1
        else:  # range _1 crosses 2 pi mark
            if phi_2 >= phi_1:  # i.e. range_2 does not cross 2 pi mark
                return [theta_1, theta_2]
            else:  # range_2 does cross 2 pi mark
                if phi_2 >= theta_1:
                    return 1  # i.e. completely masked
                elif phi_2 >= theta_2:  # overlap
                    return [theta_1, phi_2]
                elif theta_2 >= phi_2:  # overlap
                    return [theta_1, theta_2]

    def first_index_sort_ascending(self, doubles_list):
        """sorts a list of the form [[x,y],[a,b],[c,d]] by the first element of each element"""
        ascending_doubles_list = []
        while len(doubles_list) != 0:
            temp_list = []
            for i in np.arange(0, len(doubles_list), 1):
                temp_list.append((doubles_list[i])[0])
            min_index = np.argmin(temp_list)
            ascending_doubles_list.append(doubles_list[min_index])
            doubles_list.remove(doubles_list[min_index])
        return ascending_doubles_list

    def compress_masking_ranges(self, other):
        """examines ranges in the list  of masking angles ranges and compresses if there are any
        overlapping ranges; end result --> no overlapping ranges (can then use total_unmasked_range() function, assume
        that all angles are in range 0 to 2 pi and that the masking angles list is !!!!NOT EMPTY!!!"""
        # first sort all the tuples by the their first elements in ascending order
        original_list = self.masking_range()
        ref_length_1 = 1
        ref_length_2 = 0  # arbitrary initial values so that code executes while loop if len(list) > 1
        while len(original_list) != 1 and ref_length_2 < ref_length_1:
            ref_length_1 = len(original_list)
            m = -1
            original_list = self.first_index_sort_ascending(original_list)
            while m < len(original_list) - 1:  # i.e. m value is never the last element of the list
                m = m + 1
                i = m + 1  # always mth element with larger indexed elements
                while i < len(original_list):
                    if self.compare_two_ranges(original_list[m], original_list[i]) == 1:
                        return self.completely_mask_disc(other)
                    elif self.compare_two_ranges(original_list[m], original_list[i]) == 0:
                        i = i + 1
                    else:  # i.e. there is an overlap
                        new_range = self.compare_two_ranges(original_list[m], original_list[i])
                        original_list.remove(original_list[i])  # deleting higher index element first
                        original_list.remove(original_list[m])
                        original_list.append(new_range)
                        original_list = self.first_index_sort_ascending(original_list)  # need to always sort ranges by first index so that the conpare_two_ranges function can be executed
                        ref_length_2 = len(original_list)
                        m = 0  # i.e. m = 0 and i is reset to i = 1
                        break  # break out of one while loop ---> adjust m
                ref_length_2 = len(original_list)
        self.__masking_angle_ranges = original_list
        return self.__masking_angle_ranges

    def completely_mask_disc(self, other):
        """executes code when disc is to be completely masked; deleting it from surface list and adding it as a
        masked disc to lists attributed to the neighbouring discs"""
        n = self.number()
        other.delete_disc_data(n)
        self.__masking_status = "Completely Masked"
        for i in self.neighbours():
            a=other.access_disc(i)
            a.update_masked_neighbours(n)
            a.delete_neighbour(n)
        self.__masking_angle_ranges = []
        return self.__masking_angle_ranges

##############################################################################################################
############################################################################################################

class System(object):

    def __init__(self):
        self.__disc_counter=0 #counts the disc number and assigns it to each generated disc
        self.__disc_list=[] #list of disc objects
        self.__surface_coord_number = [[],[],[]] #can be extended to include variable radii
        self.__deposited_particles_tracker = 0


    def disc_number(self):
        """returns the current disc number; starts from 1 and increments sequentially"""
        return self.__disc_counter

    def increment_counter(self):
        """increments disc counter"""
        self.__disc_counter=self.__disc_counter+1

    def two_pi_limit(self, angle):
        """takes an angle and converts it to an angle between 0 and 2 pi"""
        m = np.sign(angle)
        while 1. >= 0.:
            if angle >= 2 * np.pi or angle < 0.:
                angle = angle - m*2*np.pi
            else:
                break
        return angle

    def display_stored_data(self):
        """displays the list storing surface disc coordinates and their corresponding numbers"""
        return self.__surface_coord_number

    def store_number_coordinate(self, x, y, disc_number):
        """stores disc number and x and y coordinate in a surface list to track down neighbours"""
        self.__surface_coord_number[0].append(x)
        self.__surface_coord_number[1].append(y)
        self.__surface_coord_number[2].append(disc_number)

    def delete_disc_data(self, masked_disc_number):
        """deletes a disc from the data list once it has been masked"""
        for i in np.arange(0,len(self.__surface_coord_number[2]), 1):
            if (self.__surface_coord_number[2])[i] == masked_disc_number:
                self.__surface_coord_number[0].remove((self.__surface_coord_number[0])[i])
                self.__surface_coord_number[1].remove((self.__surface_coord_number[1])[i])
                self.__surface_coord_number[2].remove((self.__surface_coord_number[2])[i])
                break

    def identify_neighbours(self, x, y, next_disc_radius):#masking angles need to be adjusted after calling this func
        """considers newly added disc and identifies neighbours"""
        surface_list = self.display_stored_data() #accesses the data
        sorted_indices_x = [i[0] for i in sorted(enumerate(surface_list[0]), key=lambda x: x[1])] #obtain indices of sorted x coords
        sorted_x_list = [[],[],[]]
        for i in sorted_indices_x: #sort data so that x list is in ascending order and the other two list contain the corresponding elements
            sorted_x_list[0].append((surface_list[0])[i])
            sorted_x_list[1].append((surface_list[1])[i])
            sorted_x_list[2].append((surface_list[2])[i])
        unsorted_y_list = [[],[],[]] #trying to find potential neighbours, [0] contains y coords and [1] contains disc numbers
        #now search for discs in the x vicinity
        for i in np.arange(0,len(sorted_indices_x), 1): #searching x coordinates from the lowest value
            if x - 4*next_disc_radius <= (sorted_x_list[0])[i]:
                m = i
                break
        for j in np.arange(m, len(sorted_indices_x),1):
            if x + 4*next_disc_radius >= (sorted_x_list[0])[j]:
                    unsorted_y_list[0].append((sorted_x_list[0])[j])
                    unsorted_y_list[1].append((sorted_x_list[1])[j])
                    unsorted_y_list[2].append((sorted_x_list[2])[j])
            else:
                break
        #now unsorted_y_list contains select range of y coordinates which are in the x vicinity along with corresponding disc numbers and x coordinates
        sorted_indices_y = [i[0] for i in sorted(enumerate(unsorted_y_list[1]), key=lambda x: x[1])]
        sorted_y_list = [[],[],[]]
        for i in sorted_indices_y:
            sorted_y_list[0].append((unsorted_y_list[0])[i])
            sorted_y_list[1].append((unsorted_y_list[1])[i])
            sorted_y_list[2].append((unsorted_y_list[2])[i])
        #now sorted_y_list contains sprted y coords and disc numbers and x coords of discs in x vicinity.
        possible_neighbours = [[],[],[]]
        for i in np.arange(0,len(sorted_indices_y),1):
            if y - 4*next_disc_radius <= (sorted_y_list[1])[i]:
                n = i
                break
        for j in np.arange(n, len(sorted_indices_y),1):
            if y + 4*next_disc_radius >= (sorted_y_list[1])[j]:
                possible_neighbours[0].append((sorted_y_list[0])[j])# i.e. append the neighbouring disc numbers
                possible_neighbours[1].append((sorted_y_list[1])[j])
                possible_neighbours[2].append((sorted_y_list[2])[j])
            else:
                break
        neighbours = []
        for k in np.arange(0, len(possible_neighbours[2]), 1):
            if (x - (possible_neighbours[0])[k])**2 + (y - (possible_neighbours[1])[k])**2 <= 16*(next_disc_radius)**2:
                neighbours.append((possible_neighbours[2])[k])
        return neighbours

    def generate_disc(self, radius, initial_x, initial_y):
        """ creates new disc object"""
        self.increment_counter()
        self.__disc_list.append(self.__disc_counter)
        self.__disc_list[self.__disc_counter-1]=Disc(self.__disc_counter, radius, initial_x, initial_y)
        self.store_number_coordinate(initial_x, initial_y, self.__disc_counter)

    def disc_list(self):
        """returns list of disc objects"""
        return self.__disc_list

    def access_disc(self, disc_number):
        """selects specified disc object from the list of disc objects; enables direct access to disc attributes"""
        return self.__disc_list[disc_number-1]

    def move_disc(self, disc_number, new_x, new_y):
        """not currently used"""
        a=self.access_disc(disc_number)
        a.change_coordinate(new_x, new_y)


    def cross_over_point(self, disc_1_x, disc_1_y, disc_1_r, disc_2_x, disc_2_y, disc_2_r, next_disc_radius):
        """takes two discs and returns crossover points in format x_cross_1, y_cross_1, x_cross_2, y_cross_2"""
        disc_1_R = disc_1_r + next_disc_radius  # taking the next_disc_radius into account, otherwise there is no overlap
        disc_2_R = disc_2_r + next_disc_radius
        c_1 = ((disc_1_R ** 2) - (disc_2_R ** 2)) - ((disc_1_x ** 2) - (disc_2_x ** 2)) - ((disc_1_y ** 2) - (disc_2_y ** 2))
        c_x = disc_1_x - disc_2_x
        c_y = disc_1_y - disc_2_y
        if c_y != 0.:
            c_2 = -(c_1) / (2 * c_y)
            c_3 = -c_x / c_y
            # now solve the quadratic equation
            A = 1 + c_3 ** 2
            B = -2 * disc_1_x + 2 * c_2 * c_3 - 2 * disc_1_y * c_3
            C = (disc_1_x ** 2) + (c_2 ** 2) - 2 * disc_1_y * c_2 + (disc_1_y ** 2) - (disc_1_R ** 2)
            p = np.array([A, B, C])
            x_cross_1, x_cross_2 = np.roots(p)  # x coordinates of crossover point
            y_cross_1_plus = disc_1_y + np.sqrt((disc_1_R) ** 2 - (x_cross_1 - disc_1_x) ** 2)
            y_cross_1_minus = disc_1_y - np.sqrt((disc_1_R) ** 2 - (x_cross_1 - disc_1_x) ** 2)
            # all the above y solutions are the correct distance from disc 1, but only one of plus/minus for y1 and y2 are correct
            # i.e. can determine which solution is correct, by computing its distance from origin of disc 2 and then see which one is smaller
            y_cross_2_plus = disc_1_y + np.sqrt((disc_1_R) ** 2 - (x_cross_2 - disc_1_x) ** 2)
            y_cross_2_minus = disc_1_y - np.sqrt((disc_1_R) ** 2 - (x_cross_2 - disc_1_x) ** 2)
            # calculating distance of points from disc 2
            m = (y_cross_1_plus - disc_2_y) ** 2 + (x_cross_1 - disc_2_x) ** 2 - disc_2_R ** 2
            n = (y_cross_1_minus - disc_2_y) ** 2 + (x_cross_1 - disc_2_x) ** 2 - disc_2_R ** 2
            p = (y_cross_2_plus - disc_2_y) ** 2 + (x_cross_2 - disc_2_x) ** 2 - disc_2_R** 2
            q = (y_cross_2_minus - disc_2_y) ** 2 + (x_cross_2 - disc_2_x) ** 2 - disc_2_R ** 2
            #then check which one makes sense
            if np.absolute(m) >= np.absolute(n):
                y_cross_1 = y_cross_1_minus
            else:
                y_cross_1 = y_cross_1_plus
            if np.absolute(p) >= np.absolute(q):
                y_cross_2 = y_cross_2_minus
            else:
                y_cross_2 = y_cross_2_plus
            return x_cross_1, y_cross_1, x_cross_2, y_cross_2
        else:
            c_4 = -(c_1) / (2 * c_x)
            # now solve the quadratic equation
            A = 1
            B = -2 * disc_1_y
            C = ((c_4 - disc_1_x) ** 2) + (disc_1_y ** 2) - (disc_1_r ** 2)
            p = np.array([A, B, C])
            y_cross_1, y_cross_2 = np.roots(p)  # y coordinates of crossover point
            # now have two solutions corresponding to y crossover coordinate
            #nultiple solutions, need to determine right one
            x_cross_1_plus = disc_1_x + np.sqrt((disc_1_r) ** 2 - (y_cross_1 - disc_1_y) ** 2)
            x_cross_1_minus = disc_1_x - np.sqrt((disc_1_r) ** 2 - (y_cross_1 - disc_1_y) ** 2)
            x_cross_2_plus = disc_1_x + np.sqrt((disc_1_r) ** 2 - (y_cross_2 - disc_1_y) ** 2)
            x_cross_2_minus = disc_1_x - np.sqrt((disc_1_r) ** 2 - (y_cross_2 - disc_1_y) ** 2)
            # checking which solutions are correct
            m = (y_cross_1 - disc_2_y) ** 2 + (x_cross_1_plus - disc_2_x) ** 2 - disc_2_r ** 2
            n = (y_cross_1 - disc_2_y) ** 2 + (x_cross_1_minus - disc_2_x) ** 2 - disc_2_r ** 2
            p = (y_cross_2 - disc_2_y) ** 2 + (x_cross_2_plus - disc_2_x) ** 2 - disc_2_r ** 2
            q = (y_cross_2 - disc_2_y) ** 2 + (x_cross_2_minus - disc_2_x) ** 2 - disc_2_r ** 2
            #checking which distance is smaller from disc 2 and selects correct point accordingly
            if np.absolute(m) >= np.absolute(n):
                x_cross_1 = x_cross_1_minus
            else:
                x_cross_1 = x_cross_1_plus
            if np.absolute(p) >= np.absolute(q):
                x_cross_2 = x_cross_2_minus
            else:
                x_cross_2 = x_cross_2_plus
            return x_cross_1, y_cross_1, x_cross_2, y_cross_2

    def vertical_angle(self, start_x, start_y, end_x, end_y):
        """calculates angle subtended by vertical and vector that points from start point to end point"""
        vector=np.array([end_x-start_x, end_y-start_y])
        normalisation_factor=np.sqrt((end_x-start_x)**2+(end_y-start_y)**2)
        normalised_vector=(np.array([end_x-start_x, end_y-start_y]))/normalisation_factor
        vertical=np.array([0,1])
        #need to determine whether normalised vector points in +x or -x direction to correctly compute angle
        if normalised_vector[0] >= 0.:
            angle=np.arccos(np.dot(vertical, normalised_vector))
        else:
            angle=2*np.pi-np.arccos(np.dot(vertical, normalised_vector))
        return angle



    def determine_masking_angles(self, other, target_disc, next_disc_x, next_disc_y, next_disc_radius, next_disc_number):# disc_1 and disc_2 refer to the disc number
        """uses cross_over_point() to determine points and then extrapolates masking angle range assuming smaller range;
        enter crossover points as [x,y]; adds masking angle range as a disc attribute for each object"""
        disc_one = self.access_disc(target_disc)
        disc_1_x = disc_one.x_coordinate() #extract required data of target disc
        disc_1_y = disc_one.y_coordinate()
        disc_1_r = disc_one.radius()
        disc_2_x = next_disc_x   #disc 2 refers to the next disc to be added to the surface
        disc_2_y = next_disc_y
        disc_2_r = next_disc_radius
        #then calculate cross over points
        x_cross_1, y_cross_1, x_cross_2, y_cross_2 = self.cross_over_point(disc_1_x, disc_1_y, disc_1_r, disc_2_x, disc_2_y, disc_2_r, next_disc_radius)
        cross_over_point_1 = [x_cross_1, y_cross_1]
        cross_over_point_2 = [x_cross_2, y_cross_2]
        #calculate angles to vertical corresponding to computed crossover points
        disc_1_angle_1 = self.vertical_angle(disc_1_x, disc_1_y, x_cross_1, y_cross_1)
        disc_1_angle_2 = self.vertical_angle(disc_1_x, disc_1_y, x_cross_2, y_cross_2)
        disc_2_angle_1 = self.vertical_angle(disc_2_x, disc_2_y, x_cross_1, y_cross_1)
        disc_2_angle_2 = self.vertical_angle(disc_2_x, disc_2_y, x_cross_2, y_cross_2)
        #now looking at the nature of the crossover angles for disc 1 to determine the clockwise orientation of the angles
        if disc_1_angle_2 > disc_1_angle_1 and disc_1_angle_2-disc_1_angle_1 <= np.pi:
            disc_one.add_masking_angles(self, [disc_1_angle_1, disc_1_angle_2]) #adding masking angles to target disc
            disc_one.add_crossover_points([cross_over_point_1,cross_over_point_2]) # adding crossover points to target disc
            disc_one.append_uncompressed_ranges([disc_1_angle_1, disc_1_angle_2], next_disc_number) #adding masking angles to uncompressed range of angle
            disc_one.update_neighbours(next_disc_number) #adding new disc as a neighbour to target disc
            return [disc_2_angle_2, disc_2_angle_1], [cross_over_point_2, cross_over_point_1] # returning same things for next disc; can be accessed from propagate func
        elif disc_1_angle_2 > disc_1_angle_1 and disc_1_angle_2-disc_1_angle_1 >= np.pi:
            disc_one.add_masking_angles(self, [disc_1_angle_2, disc_1_angle_1])
            disc_one.add_crossover_points([cross_over_point_2, cross_over_point_1])
            disc_one.append_uncompressed_ranges([disc_1_angle_2, disc_1_angle_1], next_disc_number)
            disc_one.update_neighbours(next_disc_number)
            return [disc_2_angle_1, disc_2_angle_2], [cross_over_point_1,cross_over_point_2]
        elif disc_1_angle_1 > disc_1_angle_2 and disc_1_angle_1-disc_1_angle_2 <= np.pi:
            disc_one.add_masking_angles(self, [disc_1_angle_2, disc_1_angle_1])
            disc_one.add_crossover_points([cross_over_point_2, cross_over_point_1])
            disc_one.append_uncompressed_ranges([disc_1_angle_2, disc_1_angle_1], next_disc_number)
            disc_one.update_neighbours(next_disc_number)
            return [disc_2_angle_1, disc_2_angle_2], [cross_over_point_1,cross_over_point_2]
        elif disc_1_angle_1 > disc_1_angle_2 and disc_1_angle_1-disc_1_angle_2 >= np.pi:
            disc_one.add_masking_angles(self, [disc_1_angle_1, disc_1_angle_2])
            disc_one.add_crossover_points([cross_over_point_1, cross_over_point_2])
            disc_one.append_uncompressed_ranges([disc_1_angle_1, disc_1_angle_2], next_disc_number)
            disc_one.update_neighbours(next_disc_number)
            return [disc_2_angle_2, disc_2_angle_1], [cross_over_point_2,cross_over_point_1]
        else: # for the case where the cross over points are at exactly the same point or nan error occurs
            print [disc_2_angle_2, disc_2_angle_1], [cross_over_point_2,cross_over_point_1]
            if np.isnan(disc_2_angle_1) == True or np.isnan(disc_2_angle_1) == True: #dealing with nan
                a=self.access_disc(next_disc_number)
                a.completely_mask_disc()
                other.nan_error()
            else:
                disc_one.add_masking_angles(self, [disc_1_angle_1, disc_1_angle_2])  # adding masking angles to target disc
                disc_one.add_crossover_points([cross_over_point_1, cross_over_point_2])  # adding crossover points to target disc
                disc_one.append_uncompressed_ranges([disc_1_angle_1, disc_1_angle_2], next_disc_number)  # adding masking angles to uncompressed range of angle
                disc_one.update_neighbours(next_disc_number)  # adding new disc as a neighbour to target disc
                return [disc_2_angle_2, disc_2_angle_1], [cross_over_point_2,cross_over_point_1]  # returning same things for next disc; can be accessed from propagate func

    def absolute_angle_new_disc(self, disc_number, random_angle):
        """takes the values returned in random_point(); returns absolute angle at which new disc is to be added to the
        specified surface disc; assume that the masking angles DO NOT OVERLAP here"""
        disc = self.access_disc(disc_number)
        running_total_counter = 0.
        running_total_list = [0.]
        masking_range_list = disc.masking_range()  # access masking ranges
        if len(masking_range_list) > 1:  # have to deal with multiple masking ranges
            for i in np.arange(0, len(masking_range_list), 1):
                running_total_counter = running_total_counter + self.two_pi_limit(
                    (masking_range_list[i])[0] - (masking_range_list[i - 1])[1])
                # above: calculating total angle traced out between successive masking ranges which should be in order
                running_total_list.append(self.two_pi_limit(running_total_counter))
                if random_angle <= running_total_list[i + 1]:  # checking if random_angle falls within range
                    absolute_angle = (masking_range_list[i - 1])[1] + random_angle - running_total_list[i]
                    return self.two_pi_limit(absolute_angle)
        elif len(
                masking_range_list) == 1:  # i.e. absolute angle is just clockwise of masked range plus random_angle
            return self.two_pi_limit((masking_range_list[0])[1] + random_angle)
        else:
            return random_angle  # absolute value is the random_angle

    def determine_origin(self, disc_number, random_angle, next_disc_radius):
        """used after absolute_angle_new_disc; returns origin coordinates of the new disc which can then be generated"""
        absolute_angle = self.absolute_angle_new_disc(disc_number,
                                                      random_angle)  # access absolute angle for target disc
        disc = self.access_disc(disc_number)
        disc_x = disc.x_coordinate()
        disc_y = disc.y_coordinate()
        R = disc.radius() + next_disc_radius
        new_disc_x = disc_x + R * (np.sin(absolute_angle))
        new_disc_y = disc_y + R * (np.cos(absolute_angle))  # position of newly added disc
        return new_disc_x, new_disc_y, next_disc_radius

    def extract_masked_neighbours(self, neighbours):
        """returns all masked neighbours adjacent to list of specified discs"""
        set_masked_neighbours = []
        for i in neighbours:
            a = self.access_disc(i)
            b = a.masked_neighbours() #accesses all masked neighbours of discs in neighbours
            if len(b) != 0: #i.e. if there is at least one masked disc
                for j in b:
                    set_masked_neighbours.append(j) #add to set_masked_neighbours list
            else:
                None
        c = set(set_masked_neighbours) # removes duplicate disc numbers
        return c

    def masked_neighbours_vicinity(self, neighbours, next_disc_x, next_disc_y, next_disc_radius):
        """returns list of masked discs that neighbour a specific disc, specified by coordinate and radius parameters"""
        immediate_masked_neighbours = []
        masked_neighbours = self.extract_masked_neighbours(neighbours) #all masked neighbours of the neighbours set
        if len(masked_neighbours) != 0: #i.e. if there is at least masked neighbour of the neighbours set
            for i in masked_neighbours:
                a = self.access_disc(i)
                x = a.x_coordinate()
                y = a.y_coordinate()
                r = a.radius()
                if (x-next_disc_x)**2+(y-next_disc_y)**2 < (2*r + 2*next_disc_radius)**2:
                    immediate_masked_neighbours.append(i) #append to list if it is a neighbour of the newly added disc
                else:
                    None
            return immediate_masked_neighbours
        else:
            return []

    def centre_of_mass(self):
        """returns the centre of mass"""
        a = self.disc_number()
        x_coords = np.array([])
        y_coords = np.array([])
        for i in np.arange(1, a+1, 1):
            b = self.access_disc(i)
            x = b.x_coordinate()
            y = b.y_coordinate()
            x_coords = np.append(x_coords, x)
            y_coords = np.append(y_coords, y)
        mean_x = np.mean(x_coords)
        mean_y = np.mean(y_coords)
        return mean_x, mean_y




    def roughness(self):
        """calculates and returns the roughness of the system using ALL surface discs"""
        surface_discs = (self.display_stored_data())[2] #all surface disc numbers
        x_coords = np.array([])
        y_coords = np.array([])
        for i in surface_discs:
            a = self.access_disc(i)
            x = a.x_coordinate()
            y = a.y_coordinate()
            x_coords = np.append(x_coords, x)
            y_coords = np.append(y_coords, y)

        surface_discs_radii = (x_coords**2 + y_coords**2)**0.5
        mean_radius = np.mean(surface_discs_radii)
        variance_elements = (surface_discs_radii - mean_radius)**2
        variance = np.sum(variance_elements)
        roughness = (variance**0.5)*(1/float(len(surface_discs)))
        return roughness

    def roughness_2(self):
        """calculates roughness using surface discs that are approximately spaced apart at equal angular intervals"""
        surface_discs = (self.display_stored_data())[2] #all surface disc numbers
        x_coords = np.array([]) #all the x coordinates of the surface discs
        y_coords = np.array([]) #all the y coordiantes of the surface discs
        angles_relative_to_origin = []
        disc_number = [] #keeps tracks of which discs the above arrays correspond to
        no_of_intervals = int(0.5*len(surface_discs))
        interval_size = (2*np.pi)/no_of_intervals
        for i in surface_discs:
            a = self.access_disc(i)
            x = a.x_coordinate()
            y = a.y_coordinate()
            x_coords = np.append(x_coords, x)
            y_coords = np.append(y_coords, y)
            angle = self.vertical_angle(0.,0.,x, y)
            disc_number.append(i)
            angles_relative_to_origin.append(angle)
        sorted_indices = [i[0] for i in sorted(enumerate(angles_relative_to_origin), key=lambda x: x[1])]
        sorted_angles = sorted(angles_relative_to_origin)
        sorted_disc_numbers = []
        for i in sorted_indices:
            sorted_disc_numbers.append(disc_number[i])
        selected_discs = []
        for j in np.arange(0, 2*np.pi, interval_size):
            for k in np.arange(0, len(sorted_disc_numbers), 1):
                if sorted_angles[k] > j:
                    selected_discs.append(sorted_disc_numbers[k])
                    break
                else:
                    None
        selected_x = np.array([])
        selected_y = np.array([])
        for m in selected_discs:
            a=self.access_disc(m)
            x = a.x_coordinate()
            y = a.y_coordinate()
            selected_x = np.append(selected_x, x)
            selected_y = np.append(selected_y, y)
        selected_r = (selected_x**2 + selected_y**2)**0.5
        mean_r = np.mean(selected_r)
        deviations = (selected_r - mean_r)**2
        variance = (1./len(selected_discs))*np.sum(deviations)
        roughness = np.sqrt(variance)
        return roughness

    def roughness_2_plot(self):
        """calculates roughness using surface discs that are approximately spaced apart at equal angular intervals"""
        surface_discs = (self.display_stored_data())[2]  # all surface disc numbers
        x_coords = np.array([])  # all the x coordinates of the surface discs
        y_coords = np.array([])  # all the y coordiantes of the surface discs
        angles_relative_to_origin = []
        disc_number = []  # keeps tracks of which discs the above arrays correspond to
        no_of_intervals = int(0.5 * len(surface_discs))
        interval_size = (2 * np.pi) / no_of_intervals
        for i in surface_discs:
            a = self.access_disc(i)
            x = a.x_coordinate()
            y = a.y_coordinate()
            x_coords = np.append(x_coords, x)
            y_coords = np.append(y_coords, y)
            angle = self.vertical_angle(0., 0., x, y)
            disc_number.append(i)
            angles_relative_to_origin.append(angle)
        sorted_indices = [i[0] for i in sorted(enumerate(angles_relative_to_origin), key=lambda x: x[1])]
        sorted_angles = sorted(angles_relative_to_origin)
        sorted_disc_numbers = []
        for i in sorted_indices:
            sorted_disc_numbers.append(disc_number[i])
        selected_discs = []
        for j in np.arange(0, 2 * np.pi, interval_size):
            for k in np.arange(0, len(sorted_disc_numbers), 1):
                if sorted_angles[k] > j:
                    selected_discs.append(sorted_disc_numbers[k])
                    break
                else:
                    None
        self.plot_selected_discs(selected_discs)
        self.plot_selected_discs(sorted_disc_numbers)

    def reset_system(self):
        """resets system so next simulation can be executed"""
        self.__disc_counter = 0  # counts the disc number and assigns it to each generated disc
        self.__disc_list = []  # list of disc objects
        self.__surface_coord_number = [[], [], []]  # can be extended to include variable radii

    def plot_selected_discs(self, list_disc_numbers):
        """plots selected discs"""
        fig, ax = plt.subplots()
        for i in list_disc_numbers:
            self.plot_single_disc(fig, ax, i)

    def plot_single_disc(self, fig, ax, disc_number):
        """allows plotting of selected disc(s)"""
        a = self.access_disc(disc_number)
        x_centre = a.x_coordinate()
        y_centre = a.y_coordinate()
        radius = a.radius()
        ax.add_artist(plt.Circle((x_centre, y_centre), radius, color="red"))
        ax.set_xlim((-2000, 2000))
        ax.set_ylim((-2000, 2000))

    def plot_discs(self):
        """takes all discs objects in list and plots them"""
        fig, ax = plt.subplots()
        for i in np.arange(1, len(self.disc_list())+1,1):
            a=self.access_disc(i)
            masking_ranges = a.masking_range()
            print i, masking_ranges
            x_centre=a.x_coordinate()
            y_centre=a.y_coordinate()
            radius=a.radius()
            ax.add_artist(plt.Circle((x_centre, y_centre), radius, color="%g" % float(0.000009 * a.number())))
            #ax.add_artist(plt.Circle((x_centre, y_centre), radius, color= "0.5", ec="0.01", alpha = 0.1))
            #ax.annotate(str(a.number()), xy=(x_centre, y_centre))
            ax.set_xlim((-2000, 2000))
            ax.set_ylim((-2000, 2000))
            #ax.add_artist(plt.Circle((x_centre, y_centre), radius+10, color="0.5", fill=False))
            #for j in np.arange(0, len(masking_ranges), 1):
            #    ax.add_artist(plt.Circle((x_centre+20.*np.sin(masking_ranges[j])[0], y_centre+20.*np.cos(masking_ranges[j])[0]), 0.5, color="0.1", ec="0.01", fill=False))
            #    ax.add_artist(plt.Circle((x_centre+20.*np.sin(masking_ranges[j])[1], y_centre+20.*np.cos(masking_ranges[j])[1]), 0.5, color="0.1", ec="0.01", fill=True))
        plt.show()
##############################################################################################################

class EdenADiscs(System):

    def __init__(self):
         System.__init__(self)

    def key_angles(self):
        """determines the accumulative angles of unmasked regions of the surface; returns list of accumulative angles
        with the same order as the disc objects stored in the surface list; returns list same size as surface list"""
        key_angles=[[],[]] #list of cumulative angles in first list with disc numbers in second list
        cumulative_angle=0.
        a = (self.display_stored_data())[2] #all surface disc numbers
        for i in a: #assumes only discs on surface are in disc list
            b=self.access_disc(i) #access disc
            c=float(b.total_unmasked_range()) #access total unmasked angle
            cumulative_angle=cumulative_angle+c #calculate cumulative angle
            key_angles[0].append(cumulative_angle) #append cumulative angle
            key_angles[1].append(i) #append corresponding disc number
        return key_angles

    def random_point(self):
        """computes random angle corresponding to a point on the surface; computes and returns the corresponding surface
        disc and a chosen angle, used for Eden A type model"""
        key_angles = self.key_angles() #acccess list of cumulative angles and corresponding disc angles
        #print "max random angle =", (key_angles[0])[-1]
        random_angle = np.random.uniform(0.0,(key_angles[0])[-1]) #select random angle in range of key angles
        #print "random angle=", random_angle
        #cycle through cumulative angles in key angles list and see which disc random_angle corresponds to
        for i in np.arange(0,len(key_angles[0]),1):
            if random_angle >= (key_angles[0])[i]:
                None
            else:
                #print (key_angles[1])[i], (key_angles[0])[i] - random_angle
                return (key_angles[1])[i], (key_angles[0])[i]-random_angle # returning disc number and angle to be used in absolute_angle func

    def propagate(self):
        """code to deposit one disc; only done after system class initiated and one 'seed' disc is generated"""
        i, random_angle = self.random_point()  # select random point on first disc; EITHER random_point() or random_point_2()
        next_disc_x, next_disc_y, next_disc_radius = self.determine_origin(i, random_angle, 10.)# determine origin of disc to be added
        neighbours = self.identify_neighbours(next_disc_x, next_disc_y, next_disc_radius)  # returns list of disc numbers that are neighbours
        masked_neighbours = self.masked_neighbours_vicinity(neighbours, next_disc_x, next_disc_y, next_disc_radius)
        self.generate_disc(next_disc_radius, next_disc_x, next_disc_y) #generates the next disc object
        a = self.access_disc(self.disc_number()) #enables access to the attributes of the newly created disc
        #print self.disc_number()
        for j in neighbours: #cycles through all the neighbouring disc
            a.update_neighbours(j) #accesses the neighbour
            #determines the cross over points and the corresponding masking range, appends this to target disc
            new_disc_masking_range, cross_over_points = self.determine_masking_angles(self, j, next_disc_x, next_disc_y, next_disc_radius, self.disc_number())
            a.add_masking_angles(self, new_disc_masking_range) #appending crossover points and masking range to newly added disc
            a.add_crossover_points(cross_over_points)
            a.append_uncompressed_ranges(new_disc_masking_range, j)
        if len(masked_neighbours) != 0:
            for n in masked_neighbours: #repeat for neighbours that are masked
                new_disc_masking_range, cross_over_points = self.determine_masking_angles(self, n, next_disc_x, next_disc_y, next_disc_radius, self.disc_number())
                a.add_masking_angles(self,new_disc_masking_range) # appending crossover points and masking range to newly added disc
                a.add_crossover_points(cross_over_points)
                a.append_uncompressed_ranges(new_disc_masking_range, n)
                b = self.access_disc(n)
                b.null_masking_range()#set masking ranges to []
        for k in neighbours:
            b = self.access_disc(k)
            b.compress_masking_ranges(self) #compress all the currently unmasked neighbour masking ranges
        a.compress_masking_ranges(self) #compress masking ranges of new disc

    def deposit_particles(self, number_particles):
        """deposits a specified number of discs"""
        self.__deposited_particles_tracker = number_particles
        while self.__deposited_particles_tracker > 0:
            self.propagate()
            self.__deposited_particles_tracker = self.__deposited_particles_tracker - 1

    def nan_error(self):
        """executes code if a nan_error occurs in cross_over_point function and is detected in
        determine_masking_angles() function"""
        print self.__deposited_particles_tracker
        self.deposit_particles(self.__deposited_particles_tracker) #deposits the remaining particles after nan error

#################################################################################################################

class EdenCDiscs(System):

    def __init__(self):
         System.__init__(self)

    def random_point_2(self):
        """implements Eden C type model by selecting random surface disc first and then picking site on specified disc"""
        a = (self.display_stored_data())[2] #all surface disc numbers
        b = len(a)
        c = np.random.randint(0, b)  # generates random integer between 0 and b - 1 inclusive
        target_disc_number = a[c]
        target_disc = self.access_disc(target_disc_number)
        total_unmasked_angle = float(target_disc.total_unmasked_range())  # access total unmasked angle
        random_disc_angle = np.random.uniform(0.0,total_unmasked_angle)
        return target_disc_number, random_disc_angle

    def propagate(self):
        """code to deposit one disc; only done after system class initiated and one 'seed' disc is generated"""
        i, random_angle = self.random_point_2()  # select random point on first disc; EITHER random_point() or random_point_2()
        next_disc_x, next_disc_y, next_disc_radius = self.determine_origin(i, random_angle, 10.)# determine origin of disc to be added
        neighbours = self.identify_neighbours(next_disc_x, next_disc_y, next_disc_radius)  # returns list of disc numbers that are neighbours
        masked_neighbours = self.masked_neighbours_vicinity(neighbours, next_disc_x, next_disc_y, next_disc_radius)
        self.generate_disc(next_disc_radius, next_disc_x, next_disc_y) #generates the next disc object
        a = self.access_disc(self.disc_number()) #enables access to the attributes of the newly created disc
        #print self.disc_number()
        for j in neighbours: #cycles through all the neighbouring disc
            a.update_neighbours(j) #accesses the neighbour
            #determines the cross over points and the corresponding masking range, appends this to target disc
            new_disc_masking_range, cross_over_points = self.determine_masking_angles(self, j, next_disc_x, next_disc_y, next_disc_radius, self.disc_number())
            a.add_masking_angles(self, new_disc_masking_range) #appending crossover points and masking range to newly added disc
            a.add_crossover_points(cross_over_points)
            a.append_uncompressed_ranges(new_disc_masking_range, j)
        if len(masked_neighbours) != 0:
            for n in masked_neighbours: #repeat for neighbours that are masked
                new_disc_masking_range, cross_over_points = self.determine_masking_angles(self, n, next_disc_x, next_disc_y, next_disc_radius, self.disc_number())
                a.add_masking_angles(self,new_disc_masking_range) # appending crossover points and masking range to newly added disc
                a.add_crossover_points(cross_over_points)
                a.append_uncompressed_ranges(new_disc_masking_range, n)
                b = self.access_disc(n)
                b.null_masking_range()#set masking ranges to []
        for k in neighbours:
            b = self.access_disc(k)
            b.compress_masking_ranges(self) #compress all the currently unmasked neighbour masking ranges
        a.compress_masking_ranges(self) #compress masking ranges of new disc

    def deposit_particles(self, number_particles):
        """deposits a specified number of discs"""
        self.__deposited_particles_tracker = number_particles
        while self.__deposited_particles_tracker > 0:
            self.propagate()
            self.__deposited_particles_tracker = self.__deposited_particles_tracker - 1

    def nan_error(self):
        """executes code if a nan_error occurs in cross_over_point function and is detected in
        determine_masking_angles() function"""
        print self.__deposited_particles_tracker
        self.deposit_particles(self.__deposited_particles_tracker) #deposits the remaining particles after nan error



