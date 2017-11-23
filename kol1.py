###Flight simulator. 
# Write a code in python that simulates the tilt correction of the plane (angle between plane wings and earth).
##The program should:
# - print out current orientation
# - applied tilt correction
# - run in infinite loop
# - until user breaks the loop
# Assume that plane orientation in every new simulation step is random angle with gaussian distribution (the planes is experiencing "turbulations").
# With every simulation step the orentation should be corrected, applied and printed out.
# If you can thing of any other features, you can add them.
# This code shoud be runnable with 'python kol1.py'.
# If you have spare time you can implement: Command Line Interface, generators, or even multiprocessing.
# Do your best, show off with good, clean, well structured code - this is more important than number of features.
# After you finish, be sure to UPLOAD this (add, commit, push) to the remote repository.
# Good Luck

import time
import random
from collections import namedtuple

import math

Coordinates = namedtuple('Coordinates', 'x y')
CoordinatesPolar = namedtuple('CoordinatesPolar', 'rho phi')
CoordinatesAir = namedtuple('CoordinatesAir', 'angle force')

standard_deviation = 3.0
steps_number = 10.0


class MathUtil:
    def __init__(self):
        pass

    @staticmethod
    def normalize_degrees(degrees):
        if degrees < 0:
            degrees += 360
        elif degrees >= 360:
            degrees -= 360
        return degrees

    @staticmethod
    def smallest_difference_between_angles(angle1, angle2):
        a = angle1 - angle2
        return (a + 180) % 360 - 180

    @staticmethod
    def distance_between_points(point1, point2):
        return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

    @staticmethod
    def angle_between_points(point1, point2):
        angle_in_radians = math.atan2(point2.y - point1.y, point2.x - point1.x)
        return MathUtil.polar_degrees_to_windswept(math.degrees(angle_in_radians))

    @staticmethod
    def windswept_degrees_to_polar(degrees):
        return MathUtil.normalize_degrees(450 - degrees)

    @staticmethod
    def polar_degrees_to_windswept(degrees):
        return MathUtil.normalize_degrees(450 - degrees)

    @staticmethod
    def polar_to_cartesian(rho, phi):
        x = rho * math.cos(math.radians(phi))
        y = rho * math.sin(math.radians(phi))
        return Coordinates(x, y)

    @staticmethod
    def get_random_coordinates():
        random_x = random.gauss(0.0, standard_deviation)
        random_y = random.gauss(0.0, standard_deviation)
        return Coordinates(float("{0:.1f}".format(random_x)), float("{0:.1f}".format(random_y)))


class Plane:
    plane_orientations_history = []

    def __init__(self, departure_airport_coordinates):
        self.plane_orientations_history.append(departure_airport_coordinates)

    def calculate_new_plane_orientation(self):
        new_plane_coordinate_x = random.gauss(self.plane_orientations_history[-1].x, standard_deviation)
        new_plane_coordinate_y = random.gauss(self.plane_orientations_history[-1].y, standard_deviation)
        self.plane_orientations_history.append(Coordinates(new_plane_coordinate_x, new_plane_coordinate_y))

    def get_before_plane_orientation(self):
        if len(self.plane_orientations_history) > 1:
            return self.plane_orientations_history[-2]
        else:
            return Coordinates(0.0, 0.0)

    def get_current_plane_orientation(self):
        return self.plane_orientations_history[-1]

    def correct_orientation(self, correct_orientation):
        self.plane_orientations_history[-1] = correct_orientation


class WindAutoCorrector:
    def __init__(self, departure_airport_coordinates,
                 destination_airport_coordinates):
        self.departure_airport_coordinates = departure_airport_coordinates
        self.destination_airport_coordinates = destination_airport_coordinates
        self.plane = Plane(departure_airport_coordinates)
        self.course = self.calculate_course().angle

    def calculate_course(self):
        course_angle = MathUtil.angle_between_points(
            self.departure_airport_coordinates, self.destination_airport_coordinates)
        course_force = MathUtil.distance_between_points(
            self.plane.get_before_plane_orientation(), self.calculate_expected_orientation())
        return CoordinatesAir(course_angle, course_force)

    def calculate_wind(self):
        wind_angle = MathUtil.distance_between_points(
            self.calculate_expected_orientation(), self.plane.get_current_plane_orientation())
        wind_force = MathUtil.angle_between_points(
            self.calculate_expected_orientation(), self.plane.get_current_plane_orientation())
        return CoordinatesAir(wind_angle, wind_force)

    def calculate_expected_orientation(self):
        x_step = (self.destination_airport_coordinates.x - self.departure_airport_coordinates.x) / steps_number
        y_step = (self.destination_airport_coordinates.y - self.departure_airport_coordinates.y) / steps_number
        x = self.plane.get_before_plane_orientation().x + x_step
        y = self.plane.get_before_plane_orientation().y + y_step
        return Coordinates(x, y)

    def calculate_course_after_correction(self):
        x = self.plane.get_before_plane_orientation().x
        y = self.plane.get_before_plane_orientation().y

        wind_direction_in_cartesian = MathUtil.polar_to_cartesian(
            self.calculate_wind().force,
            MathUtil.windswept_degrees_to_polar(self.calculate_wind().angle)
        )
        x += wind_direction_in_cartesian.x
        y += wind_direction_in_cartesian.y

        course_angle = MathUtil.angle_between_points(Coordinates(x, y), self.calculate_expected_orientation())
        course_force = MathUtil.distance_between_points(Coordinates(x, y), self.calculate_expected_orientation())

        return CoordinatesAir(course_angle, course_force)

    def calculate_wind_correction_angle(self):
        return MathUtil.smallest_difference_between_angles(self.calculate_course_after_correction().angle, self.course)

    def simulate_current_orientation(self):
        x = self.plane.get_before_plane_orientation().x
        y = self.plane.get_before_plane_orientation().y

        course_direction_in_cartesian = MathUtil.polar_to_cartesian(
            self.calculate_course_after_correction().force,
            MathUtil.windswept_degrees_to_polar(self.calculate_course_after_correction().angle)
        )

        x += course_direction_in_cartesian.x
        y += course_direction_in_cartesian.y

        wind_direction_in_cartesian = MathUtil.polar_to_cartesian(
            self.calculate_wind().force,
            MathUtil.windswept_degrees_to_polar(self.calculate_wind().angle)
        )

        x += wind_direction_in_cartesian.x
        y += wind_direction_in_cartesian.y

        correct_orientation = Coordinates(float("{0:.3f}".format(x)), float("{0:.3f}".format(y)))

        self.plane.correct_orientation(correct_orientation)

        return correct_orientation

    def is_not_end_of_flight(self):
        return self.plane.get_current_plane_orientation() != self.destination_airport_coordinates


class FlightSimulator:
    def __init__(self):
        self.wind_auto_corrector = WindAutoCorrector(Coordinates(0.0, 0.0), MathUtil.get_random_coordinates())
        self.simulation_delay = 1.0

    def start(self):
        while self.wind_auto_corrector.is_not_end_of_flight():
            print "_____________________________________________________________________________"
            print("\n\tDEPARTURE AIRPORT: (%s,%s) \t DESTINATION AIRPORT: (%s,%s)"
                  % (self.wind_auto_corrector.departure_airport_coordinates.x,
                     self.wind_auto_corrector.departure_airport_coordinates.y,
                     self.wind_auto_corrector.destination_airport_coordinates.x,
                     self.wind_auto_corrector.destination_airport_coordinates.y)
                  )

            print "_____________________________________________________________________________"
            self.wind_auto_corrector.plane.calculate_new_plane_orientation()

            print("\n\tCOURSE: %0.2f%s \t WIND %0.2f%s/%0.2f"
                  % (self.wind_auto_corrector.calculate_course().angle, unichr(176),
                     self.wind_auto_corrector.calculate_wind().angle, unichr(176),
                     self.wind_auto_corrector.calculate_wind().force)
                  )

            print("\n\tCURRENT ORIENTATION: (%0.1f,%0.1f)"
                  % (self.wind_auto_corrector.plane.get_current_plane_orientation().x,
                     self.wind_auto_corrector.plane.get_current_plane_orientation().y))

            print "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _"

            print("\n\tWIND CORRECTION ANGLE: %0.2f%s \t COURSE AFTER CORRECTION: %0.2f%s"
                  % (self.wind_auto_corrector.calculate_wind_correction_angle(), unichr(176),
                     self.wind_auto_corrector.calculate_course_after_correction().angle, unichr(176)))
            print "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _"

            print("ORIENTATION:")
            print("\n\tEXPECTED:(%s, %s) \t SIMULATED: (%s, %s)"
                  % (self.wind_auto_corrector.calculate_expected_orientation().x,
                     self.wind_auto_corrector.calculate_expected_orientation().y,
                     self.wind_auto_corrector.simulate_current_orientation().x,
                     self.wind_auto_corrector.simulate_current_orientation().y))
            print "_____________________________________________________________________________"

            time.sleep(self.simulation_delay)


if __name__ == "__main__":

    print "*********************************************"
    print("\n\tWelcome to flight simulator!\n")
    print "*********************************************"

    raw_input("Press Enter to generate new simulation...\n")

    try:
        while True:
            print "*********************************************"
            flight_simulator = FlightSimulator()
            flight_simulator.start()
            print "*********************************************"
            print("\nPress ctrl + c to exit")
            raw_input("\nPress Enter to generate new simulation...\n")

    except KeyboardInterrupt:
        exit()
