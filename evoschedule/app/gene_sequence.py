class GeneSequence:
    def __init__(self,
                sequence,
                heuristic,
                max_mutation_rate):
        """ This class represents a single gene sequence.
        
        A gene sequence is composed of tasks. Each spot in the sequence,
        known as an allele, can be one of several genes specified by the 
        Genome class."""
        
        self.sequence = sequence
        self.length = len(sequence)
        self.heuristic = heuristic
        self.max_mutation_rate = max_mutation_rate
        self.fitness = self.heuristic.get_fitness(self.sequence)



    def get_mutated(self):
        """ Generates the child sequence of this sequence."""

        from random import randint
        from math import ceil
        
        max_swaps = ceil(self.max_mutation_rate * self.length)
        n_swaps = randint(0, max_swaps)

        mutated = list(self.sequence) # copy
 
        for i in range(n_swaps):
            a = randint(0, self.length - 1)
            b = randint(0, self.length - 1)
            mutated[a], mutated[b] = mutated[b], mutated[a]

        mutated_gene_sequence = GeneSequence(mutated, 
                                            self.heuristic, 
                                            self.max_mutation_rate)
        return mutated_gene_sequence

    def consolidate_schedule(self):
        """ Combines same task in adjacent time windows to a single time frame.
        i.e.,   12:00AM - 01:00PM - Sleep
                01:00PM - 02:00PM - Sleep
                02:00PM - 03:00PM - Sleep
                03:00PM - 04:00PM - Sleep
                04:00PM - 05:00PM - Sleep
                
        gets combined into
                12:00AM - 05:00PM - Sleep"""

        time_windows = self.heuristic.time_windows
        
        task = self.sequence[0]
        start = time_windows[0][0]        
        time_frames = []
        for i in range(len(time_windows)):
            if self.sequence[i] != task:
                end = time_windows[i][0]
                time_frames.append((start, end, task))
                task = self.sequence[i]
                start = time_windows[i][0]
        end = time_windows[0][0]
        time_frames.append((start, end, task))
        return time_frames

    def get_schedule(self):
        """ Returns the consolidated schedule."""

        s = ""
        for time_frame in self.consolidate_schedule():
            start = time_frame[0]
            end = time_frame[1]
            task = time_frame[2]
            s += f"{start:10s} - {end:10s} === {task:10s}\n"
        return s

    def schedule(self):
        return self.consolidate_schedule()

    def __str__(self):
        return str(self.sequence)
