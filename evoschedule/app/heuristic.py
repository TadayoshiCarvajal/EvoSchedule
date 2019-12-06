class Heuristic:
    def __init__(self, H, genome, time_windows):
        """ An object which tells us information about what constitutes
        a good sequence. A good sequence will have a fitness that is closer
        to the global maximum as given by the Hungarian Algorithm."""
        
        self.H = H
        self.time_slot_size = genome.allele_size
        self.genes_per_task = genome.genes
        self.matrix_row_to_task = {}
        self.cost_matrix = self.get_cost_matrix()
        self.optimal_matching = self.hungarian_algorithm()
        self.optimal_sequence = self.get_optimal_sequence()
        self.optimal_fitness = self.get_fitness(self.optimal_sequence, ratio=False)
        self.time_windows = time_windows
        

    def get_fitness(self, sequence, ratio=True):
        """ Returns the fitness of a specified sequence.
        
        ratio=True means the fitness is expressed a ratio.
        ratio=False means the absolute fitness is returned."""

        fitness = 0
        for idx, task in enumerate(sequence):
            fitness += self.H[task][idx]
        if ratio:
            return fitness / self.optimal_fitness
        else:
            return fitness

    def get_cost_matrix(self):
        """ Sets the weight matrix and returns the cost matrix.
        
        The cost matrix is just each value from the weight matrix
        subtracted from the max value (10). This is done because
        the hungarian algorithm solves for the shortest cost complete
        bipartite matching of tasks to time slots."""

        from numpy import matrix
        import numpy as np
        np.set_printoptions(threshold=np.inf)
        M = []
        j = 0
        for task in self.H:
            for i in range(self.genes_per_task[task]):
                row = list(self.H[task])
                M.append(row)
                self.matrix_row_to_task[j] = task
                j += 1

        self.weight_matrix = matrix(M)

        return 10 - matrix(M)

    def hungarian_algorithm(self):
        """ An algorithm for solving the assignment problem.
        
        The Assignment problem is sometimes called the min-cost 
        perfect bipartite matching problem. This algorithm returns 
        the optimal sequence of tasks and time slots given our 
        heuristics matrix H expressed as a cost_matrix."""

        from scipy import optimize
        return optimize.linear_sum_assignment(self.cost_matrix)

    def get_optimal_sequence(self):
        """ Uses the output of the hungarian algorithm to produce the optimal
        sequence."""

        optimal_row, optimal_col = self.optimal_matching
        n = len(optimal_row)
        optimal_assignment = self.cost_matrix[optimal_row,optimal_col]
        optimal_task = []
        optimal_time = []

        for i in range(n):
            optimal_task.append(self.matrix_row_to_task[optimal_row[i]])
            optimal_time.append(optimal_col[i]*self.time_slot_size)
        
        optimal_seq = list(list(zip(*sorted(zip(optimal_time, optimal_task))))[1])
        return optimal_seq