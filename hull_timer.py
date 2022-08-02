"""
    File:        hull_timer.py
    Author:      Darren Strash
    Course:      CS 307 - Computational Geometry
    Semester:    Spring 2022
    Assignment:  Problem Set 1 - Convex Hulls
    Description: Execute different hull algorithms (implemented by
    you!) and print out a table of times to show growth rates.
"""

from hull import generate_points
from hull import slow_convex_hull
from hull import graham_scan
from hull import jarvis_march

import datetime

NUM_ITERATIONS = 3

def average_time(hull_algorithm, points):
    """call hull_algorithm on points repeatedly and return average time"""
    time_diff = None

    for iteration in range(0, NUM_ITERATIONS):
        points_copy = points[:]
        start = datetime.datetime.now()
        hull_algorithm(points_copy)
        end = datetime.datetime.now()
        if time_diff == None:
            time_diff = end - start
        else:
            time_diff = time_diff + end - start

    time_ms = time_diff.microseconds // 1000
    time_ms = time_ms + time_diff.seconds * 1000
    time_ms = time_ms + time_diff.days * 24 * 60 * 60 * 1000

    return time_ms

def get_table_entry(num_points, points_on_hull, item):
    """get the appropriate table entry, which is either a number of points
       or a running time"""
    points = generate_points(num_points, points_on_hull)
    if item == "n":
        return num_points
    elif item == "h":
        return points_on_hull
    elif item == "slow":
        return average_time(slow_convex_hull, points) 
    elif item == "jarvis":
        return average_time(jarvis_march, points) 
    elif item == "graham":
        return average_time(graham_scan, points) 
        
    return -1

def build_header_and_legend(option):
    """construct the header entries, which are also used to fill table entries"""
    # always print n (number of vertices)
    header = ["n"]

    print("Legend:")
    print("    n      : the number of points")

    if option == "hullsize":
        header.append("h")
        print("    h      : the number of points on the convex hull")

    if option == "all" or option == "noslow" or option == "onlygraham":
        header.append("graham")
        print("    graham : the running time of Graham's Scan (in ms)")

    if option == "all" or option == "noslow" or option == "hullsize":
        header.append("jarvis")
        print("    jarvis : the running time of Jarvis's March (in ms)")
    
    if option == "all":
        header.append("slow")
        print("    slow   : the running time of Brute Force (in ms)")

    print("")

    return header

def run_experiment(option):
    """run the timing experiement according to the user-supplied option"""
    header = build_header_and_legend(option)

    for item in header:
        print("{:>15} ".format(item), end="")
    print("")

    for i in range(2,35):
        size = 2**i
        hull_size = size
        if option == "hullsize":
            hull_size = 4

        while hull_size <= size:
            for item in header:
                print("{:>15} ".format(get_table_entry(size, hull_size, item)), end="")
            hull_size = 2 * hull_size
            print("")

        if option == "hullsize":
            print("")


def main():
    """Get user input and run appropriate timing experiment."""
    print("Welcome to Hull Timer! Press Ctrl+C at any time to end...")

    option = input("Which test would you like to run (all,noslow,onlygraham,hullsize)? ")
    while option not in ["all", "noslow", "onlygraham", "hullsize"]:
        print("Unrecognized option '", option, "'")
        option = input("Which test would you like to run? (all,noslow,onlygraham,hullsize)")

    if option == "all":
        print("Running all algorithms with n vertices on hull.")
        print("This test includes the slow algorithm. Run 'noslow' to remove it.")
    elif option == "noslow":
        print("Running all algorithms except the slow algorithm, with n vertices on hull.")
    else:
        print("Running only Jarvis March and varying hull size.")

    run_experiment(option)

if __name__ == "__main__":
    main()
