from timeit import default_timer as timer
from map_coloring_csp import Map

class Test:
    def __init__(self, map_coloring_csp, average, colors):
        self.csp = map_coloring_csp
        self.average = average
        self.colors = colors

    def test(self, increment, max_size):
        for n in range(increment, max_size, increment):
            pass


    def test_min_conflicts(self, n, max_steps):
        timeArray = []
        num_of_times_solved = 0
        for _ in range(self.average):
            self.csp.initialize_map(n)
            start = timer()
            self.csp.min_conflicts(max_steps, self.colors)
            end = timer()
            if self.csp.validateSolution():
                num_of_times_solved += 1
            timeArray.append(end - start)

        time_mean = sum(timeArray)/self.average
        return time_mean, (num_of_times_solved/self.average) * 100

    def test_constraint_weighting(self, n, max_steps, weight_increment):
        timeArray = []
        num_of_times_solved = 0
        for _ in range(self.average):
            self.csp.initialize_map(n)
            start = timer()
            self.csp.constraint_weighting(max_steps, self.colors, weight_increment)
            end = timer()
            if self.csp.validateSolution():
                num_of_times_solved += 1
            timeArray.append(end - start)

        time_mean = sum(timeArray)/self.average
        return time_mean, (num_of_times_solved/self.average) * 100

