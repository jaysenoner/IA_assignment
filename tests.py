from timeit import default_timer as timer
import matplotlib.pyplot as plt

from csp_generator import cspGenerator
from map_coloring_csp import Map
from tabulate import tabulate


class Test:
    def __init__(self, average, colors, max_steps):
        self.csp = Map()
        self.average = average
        self.colors = colors
        self.max_steps = max_steps

    def test_all_and_plot(self, increment, max_size):
        xs, ys, percentage_solved = self.test_(increment, max_size, 0)
        plt.plot(xs, ys)
        min_cf_ys = ys
        print(percentage_solved)
        xs, ys, percentage_solved = self.test_(increment, max_size, 1)
        print(percentage_solved)
        plt.plot(xs, ys)
        plt.title("min conflicts and constraint weighting")
        plt.xlabel("Number of variables")
        plt.ylabel("Time elapsed")
        plt.legend(["min_conflicts", "constraint-weighting"])
        plt.show()
        table = {"Dimensione CSP ": [round(value, 6) for value in xs],
                 "min_conflicts(ms)": [round(value, 6) * 1000 for value in min_cf_ys],
                 "constraint_weighting(ms)": [round(value, 6) * 1000 for value in ys]

                 }
        print(tabulate(table, headers='keys', tablefmt="latex_longtable"))

    def test_and_plot(self, increment, max_size, solver):
        xs, ys, percentage_solved = self.test_(increment, max_size, solver)
        plt.plot(xs, ys)
        plt.xlabel("Number of variables")
        plt.ylabel("Time elapsed")
        if solver == 0:
            plt.title("min_conflicts on average of "
                      + str(self.average) + " trials")
        elif solver == 1:
            plt.title("constraint weighting on average of "
                      + str(self.average) + " trials")
        print("Percentage of problems solved for each value of n", end="")
        print(percentage_solved)
        plt.show()

    def test_(self, increment, max_size, solver):
        time_array = []
        percentage_array = []
        for i, n in enumerate(range(increment, max_size + increment, increment)):
            print("Progress:" + str(i))
            if solver == 0:
                time, percentage_solved = self.test_min_conflicts(n)
            else:
                time, percentage_solved = self.test_constraint_weighting(n)
            time_array.append(time)
            percentage_array.append(percentage_solved)

        dimension_array = list(range(increment, max_size + increment, increment))
        return dimension_array, time_array, percentage_array

    def test_min_conflicts(self, n):
        time_array = []
        num_of_times_solved = 0
        for _ in range(self.average):
            self.csp.initialize_map(n)
            start = timer()
            self.csp.min_conflicts(self.max_steps, self.colors)
            end = timer()
            if self.csp.validateSolution():
                num_of_times_solved += 1
            time_array.append(end - start)

        time_mean = sum(time_array) / self.average
        return time_mean, (num_of_times_solved / self.average) * 100

    def test_constraint_weighting(self, n, weight_increment=10):
        time_array = []
        num_of_times_solved = 0
        for _ in range(self.average):
            self.csp.initialize_map(n)
            start = timer()
            self.csp.constraint_weighting(self.max_steps, self.colors, weight_increment)
            end = timer()
            if self.csp.validateSolution():
                num_of_times_solved += 1
            time_array.append(end - start)

        time_mean = sum(time_array) / self.average
        return time_mean, (num_of_times_solved / self.average) * 100

    def solve_and_print(self, n, solver, weight_increment=2):
        points, lines = self.csp.initialize_map(n)
        cspGenerator.plot_graphical_csp(points, lines, True)
        self.csp.printMap()
        print("\n")
        if solver == 0:
            self.csp.min_conflicts(self.max_steps, self.colors)
        else:
            self.csp.constraint_weighting(self.max_steps, self.colors, weight_increment)
        if self.csp.validateSolution():
            print("Solution found")
            print("Solved map coloring CSP:")
            self.csp.printMap(False)
        else:
            print("Solution not found")
