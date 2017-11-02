###Flight simulator. 
#Write a code in python that simulates the tilt correction of the plane (angle between plane wings and earth). 
##The program should:
# - print out current orientation
# - applied tilt correction
# - run in infinite loop
# - until user breaks the loop
#Assume that plane orientation in every new simulation step is random angle with gaussian distribution (the planes is experiencing "turbulations"). 
#With every simulation step the orentation should be corrected, applied and printed out.
#If you can thing of any other features, you can add them.
#This code shoud be runnable with 'python kol1.py'.
#If you have spare time you can implement: Command Line Interface, generators, or even multiprocessing.
#Do your best, show off with good, clean, well structured code - this is more important than number of features.
#After you finish, be sure to UPLOAD this (add, commit, push) to the remote repository.
#Good Luck

import time
import random

standard_deviation = 20.0
right_plane_orientation= 5.0

correction_delay = 1.5

def calculate_current_plane_orientation(previous_plane_orientation) :
	return random.gauss(previous_plane_orientation, standard_deviation)

def calculate_tilt_correction(current_plane_orientation) :
	return right_plane_orientation - current_plane_orientation

def plane_orientation_after_correction(current_plane_orientation, tilt_correction) :
	return current_plane_orientation + tilt_correction

try:
	current_plane_orientation = right_plane_orientation

	while True:
	    current_plane_orientation = calculate_current_plane_orientation(current_plane_orientation)
	    tilt_correction = calculate_tilt_correction(current_plane_orientation)

	    print("[%s] - current plane orientation" % current_plane_orientation)
	    print("[%s] - tilt correction" % tilt_correction)

	    current_plane_orientation = plane_orientation_after_correction(current_plane_orientation, tilt_correction)

	    print("[%s] - plane orientation after correction \n" % current_plane_orientation)
	    
	    time.sleep(correction_delay)

except KeyboardInterrupt:
	exit()
