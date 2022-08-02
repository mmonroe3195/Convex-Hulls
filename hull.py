"""
    File:        hull.py
    Author:      Madison Monroe
    Course:      CS 307 - Computational Geometry
    Semester:    Spring 2022
    Assignment:  Problem Set 1 - Convex Hulls
    Description: Methods to generate points and compute convex hulls
    with different algorithms.
"""
import math
import random

def valid_point_list(points):
    """Determines whether a list of points is valid. It is valid if there are
       more than 3 unique points"""
    points = list(set(points))

    if  len(points) < 3:
        return False

    return True

def orient(p, q, r):
    """Determines whether point r is on the left, right, or collinear with p and
       q. Returns 1 if the point is to the left, -1 if it is to the right,
       and 0 if the point is collinear"""
    #splits tuple of points to get x and y coordinates
    px, py = p
    qx, qy = q
    rx, ry = r

    #finds the determinate as was done in class
    determinate = qx * ry + px * qy + rx * py - qx * py - rx * qy - ry * px

    if determinate > 0:
        return 1

    elif determinate < 0:
        return -1

    return 0

def slope(p, q):
    """Determines the slope given two points"""
    px, py = p
    qx, qy = q

    if px - qx == 0:
        return None

    return (py - qy) / (px - qx)

def collinear(p, q, r):
    """Determines if 3 points are collinear by comparing slopes"""

    if slope(p,q) == slope(q,r) and slope(p,q) == slope(p,r):
        return True

    return False

def generate_points(num_points, points_on_hull):
    """Generate a set of num_points points with points_on_hull points
       on its convex hull"""

    if points_on_hull > num_points or num_points < 0 \
       or points_on_hull < 0 or points_on_hull < 3:
        return None

    points = []

    x_coordinate = 0
    highest_hull_y = 0

    #calculating the points on the convex hull
    while len(points) != points_on_hull - 2:
        """done so that the top pts on the left and on the right of the parabola
         always have the same y value"""
        if x_coordinate == 0 and points_on_hull % 2 == 0:
            x_coordinate += 1

        # points on the hull will be caclulated with quadradic fn y = x^2
        y_coordinate = pow(x_coordinate, 2)
        highest_hull_y = y_coordinate
        points.append((x_coordinate, y_coordinate))

        if x_coordinate != 0:
            points.append((-x_coordinate, y_coordinate))

        x_coordinate += 1

    x_coordinate = 0
    highest_nonhull_y = 0
    y_coordinate = 2

    # determining the points inside the convex hull
    while len(points) < num_points - 2:
        points.append((x_coordinate, y_coordinate))
        highest_nonhull_y = y_coordinate

        y_coordinate += 1

    """the last two points on the hull are calculated after the points inside
    the hull are calculated. This is to ensure that none of the inner points
    have a y coordinate greater than the highest y coordinate for points
    on the hull"""
    if highest_nonhull_y >= highest_hull_y:
        #calculating the next x coordinate based on the highest_hull_y
        x_coordinate = int(math.ceil(math.sqrt(highest_nonhull_y))) + 1
        y_coordinate = pow(x_coordinate, 2)
        points.append((x_coordinate, y_coordinate))
        points.append((-x_coordinate, y_coordinate))

    else:
        x_coordinate = int(math.sqrt(highest_hull_y) + 1)
        y_coordinate = pow(x_coordinate, 2)
        points.append((x_coordinate, y_coordinate))
        points.append((-x_coordinate, y_coordinate))

    return points

def slow_convex_hull(points):
    """compute the convex hull of points in O(n^3) time"""

    if not valid_point_list(points):
        return None

    edges = []
    convex_hull = []

    for p in points:
        for q in points:
            if p != q:
                valid = True

                for r in points:
                    if r != q and r != p:
                        if orient(p, q, r) == 1:
                            valid = False
                            break

                if valid:
                    edges.append((p,q))

    #using the list of edges to construct the list of points on the convex hull
    p, q = edges[0]
    convex_hull.append(p)
    convex_hull.append(q)
    edges.pop(0)

    while len(edges) > 1:
        for index in range(len(edges)):
            if edges[index] != 0:
                p, q = edges[index]

                if p == convex_hull[-1]:
                    convex_hull.append(q)
                    edges.pop(index)
                    break

    return convex_hull

def graham_scan(points):
    """Run Graham Scan on points in O(n log n) time"""

    if not valid_point_list(points):
        return None

    upper_hull = []
    lower_hull = []

    points.sort()

    #adding the first two points in the upper hull
    upper_hull.append(points[0])
    upper_hull.append(points[1])

    for index in range(2, len(points)):
        upper_hull.append(points[index])

        while len(upper_hull) > 2 and orient(upper_hull[-3], upper_hull[-2], upper_hull[-1]) != -1:
            upper_hull.pop(-2)

    #adding first two points in the lower hull
    lower_hull.append(points[-1])
    lower_hull.append(points[-2])

    for index in range((len(points) - 2), -1, -1):
        lower_hull.append(points[index])

        while len(lower_hull) > 2 and orient(lower_hull[-3], lower_hull[-2], lower_hull[-1]) != -1:
            lower_hull.pop(-2)

    #popping the points that are already in the upper_hull
    lower_hull.pop(-1)
    lower_hull.pop(0)

    convex_hull = upper_hull + lower_hull

    return convex_hull

def jarvis_march(points):
    """Run Jarvis March on points in O(nh) time"""

    if not valid_point_list(points):
        return None

    convex_hull = []
    points.sort()
    convex_hull.append(points[0])
    remaining_points = points[1:]

    while True:
        for next_hull_point in remaining_points:
            valid = True

            prev_hull_point = convex_hull[-1]

            #checking if each point is to the right of the line segment
            for j in range(len(points)):
                if next_hull_point != points[j] and prev_hull_point != points[j]:

                    if orient(prev_hull_point, next_hull_point, points[j]) == 1:
                        valid = False
                        break

            if valid:
                convex_hull.append(next_hull_point)

                if next_hull_point == convex_hull[0]:
                    convex_hull.pop()
                    return convex_hull

            remaining_points = []

            for value in points:
                if value not in convex_hull:
                    remaining_points.append(value)
            remaining_points.append(convex_hull[0])

def test():
    points = generate_points(50,3)
    print(points)
    print(slow_convex_hull(points))
    print(graham_scan(points))
    print(jarvis_march(points))

    for _ in range(25):
        points_on_hull = random.randint(3, 70)
        num_points = points_on_hull + random.randint(0, 70)
        points = generate_points(num_points, points_on_hull)
        hull1 = jarvis_march(points)
        hull2 = graham_scan(points)
        hull3 = slow_convex_hull(points)

        if hull3 != hull2 or hull1 != hull3:
            print("Potential Error. Please compare.")
            print(points)
            print(" Hull 1: ")
            print(hull1)
            print(" Hull 2: ")
            print(hull2)
            print(" Hull 3: ")
            print(hull3)
