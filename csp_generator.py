import shapely
import numpy as np
from shapely.geometry import LineString
from shapely.geometry import Point
import matplotlib.pyplot as plt


"""
       Generate random instances of map-coloring problems as follows: scatter 
       n points on the unit square; select a point X at random, connect X by a straight line to the nearest point Y such that 
       X is not already connected to Y and the line crosses no other line; 
       repeat the previous step until no more connections are possible. 
       The points represent regions on the map and the lines connect neighbors. 
"""

class cspGenerator:

    @staticmethod
    def line_intersects(existing_line, new_line, points):
        existing_line_first = Point(existing_line.coords[0])
        existing_line_last = Point(existing_line.coords[-1])
        new_line_first = Point(new_line.coords[0])
        new_line_last = Point(new_line.coords[-1])

        intersection = shapely.intersection(existing_line, new_line)
        # Check if the intersection is one of the points of the graph. if that is the case, we check if
        # there is any connection between segments that generated such intersection, and we return false
        # if we find out that the 2 segment are connected by one of their endpoints. Otherwise, we return True
        if any(intersection.equals(point) for point in points):
            if existing_line_first.equals(new_line_first) or existing_line_first.equals(new_line_last) \
                    or existing_line_last.equals(new_line_first) or existing_line_last.equals(new_line_last):
                return False
            else:
                return True
        # Here we check if the line that we are creating passes through a point in the graph, excluding the points of
        # the new line
        all_points_except_endpoints = [point for point in points if
                                       not (point.equals(new_line_first) or point.equals(new_line_last))]
        if any(new_line.distance(point) < 0.0001 for point in all_points_except_endpoints):
            return True

        return existing_line.intersects(new_line)

    @staticmethod
    def generate_random_graphical_csp(n):
        created_constraints = []

        points = np.random.random((n, 2))
        shapely_points = [shapely.Point(point[0], point[1]) for point in points]

        i = 0
        calculate_distances = True
        distances = []
        while True:
            # print("progress:" + str(i)) Uncomment to show progress while creating graphical csp
            if i > len(shapely_points) - 1:
                break
            if calculate_distances:
                distances = [shapely_points[i].distance(other_point) for other_point in shapely_points]
            distances[i] = np.inf
            nearest_point = shapely_points[np.argmin(distances)]
            expected_line = LineString([shapely_points[i], nearest_point])

            if not any(
                    line.equals(expected_line) or cspGenerator.line_intersects(line, expected_line, shapely_points) for
                    line in
                    created_constraints):
                created_constraints.append(expected_line)
                i += 1
                calculate_distances = True
            else:
                distances[shapely_points.index(nearest_point)] = np.inf
                calculate_distances = False

            if all(distance == np.inf for distance in distances):
                i += 1
                calculate_distances = True

        return shapely_points, created_constraints

    @staticmethod
    def plot_graphical_csp(created_variables, created_constraints, show_labels):

        xs = [point.x for point in created_variables]
        ys = [point.y for point in created_variables]
        for i in range(len(created_constraints)):
            x, y = created_constraints[i].xy
            plt.plot(x, y)
        plt.scatter(xs, ys)

        # Code that I got from pyplotlib documentation to give a label to each point
        if show_labels:
            for idx, (x, y) in enumerate(zip(xs, ys)):
                label = idx

                plt.annotate(label,  # this is the text
                             (x, y),  # these are the coordinates to position the label
                             textcoords="offset points",  # how to position the text
                             xytext=(0, 10),  # distance from text to points (x,y)
                             ha='center')  # horizontal alignment can be left, right or center
        plt.show()

