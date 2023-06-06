from shapely import Point
import random
from csp_generator import cspGenerator


class Region:
    def __init__(self, name, color=None):
        self.name = name
        self.color = color
        self.neighbors = []

    def add_neighbor(self, region):
        if region not in self.neighbors:
            self.neighbors.append(region)
            region.add_neighbor(self)

    def printRegion(self):
        print(self.name, end="")
        if self.color is not None:
            print("," + self.color)


class Map:
    def __init__(self):
        self.regions = []

    def printMap(self, print_neighbors=True):
        for region in self.regions:
            print()
            region.printRegion()
            if print_neighbors:
                firstTime = True
                for neighbor in region.neighbors:
                    if firstTime:
                        print(":", end="")
                        firstTime = False
                    neighbor.printRegion()
                    print(",", end="")

    def add_region(self, region):
        self.regions.append(region)

    def initialize_map(self, n):
        points, lines = cspGenerator.generate_random_graphical_csp(n)
        self.regions = [Region(i) for i in range(n)]

        i = 0
        while i < n:
            neighbors = [line for line in lines if
                         Point(line.coords[0]).equals(points[i]) or Point(line.coords[-1]).equals(points[i])]
            for neighbor in neighbors:
                if Point(neighbor.coords[0]).equals(points[i]):
                    self.regions[i].add_neighbor(Region(self.findIndexOfPoint(points, Point(neighbor.coords[-1]))))
                else:
                    self.regions[i].add_neighbor(Region(self.findIndexOfPoint(points, Point(neighbor.coords[0]))))
            i += 1
        return points, lines

    def findIndexOfPoint(self, points, point_to_check):
        for index, point in enumerate(points):
            if point.equals(point_to_check):
                return index

    def validateSolution(self):
        validSolution = True
        for region in self.regions:
            for neighbor in region.neighbors:
                if region.color == neighbor.color:
                    validSolution = False
                    break

        return validSolution

    # Solvers
    def min_conflicts(self, max_steps, colors):
        for region in self.regions:
            region.color = random.choice(colors)
        for i in range(max_steps):
            conflicted_regions = [r for r in self.regions if any(r.color == n.color for n in r.neighbors)]
            if not conflicted_regions:
                return self
            region = random.choice(conflicted_regions)
            region.color = min(colors, key=lambda color: sum(n.color == color for n in region.neighbors))
        return None

    def constraint_weighting(self, max_steps, colors, weight_increment):
        weights = {region: 1 for region in self.regions}
        for region in self.regions:
            region.color = random.choice(colors)
        for i in range(max_steps):
            conflicted_regions = [r for r in self.regions if any(r.color == n.color for n in r.neighbors)]
            if not conflicted_regions:
                return self
            region = max(conflicted_regions, key=lambda r: weights[r] * sum(r.color == n.color for n in r.neighbors))
            region.color = min(colors, key=lambda color: sum(n.color == color for n in region.neighbors))
            weights[region] += weight_increment
        return None



