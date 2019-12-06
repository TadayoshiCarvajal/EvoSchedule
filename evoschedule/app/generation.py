class Generation:
    def __init__(self,
                genome, 
                heuristic, 
                seqs_per_gen, 
                breed_rate, 
                max_mutation_rate):
        """ A collection of GeneSequences which provides some helpful
        utility methods. """

        self.genome = genome
        self.heuristic = heuristic
        self.seqs_per_gen = seqs_per_gen
        self.breed_rate = breed_rate
        self.max_mutation_rate = max_mutation_rate
        self.members = []

    def generate_members(self):
        """ Generates the members of the first generation."""

        from app.gene_sequence import GeneSequence

        for i in range(self.seqs_per_gen):
            seq = GeneSequence(self.genome.get_random_sequence(),
                                self.heuristic,
                                self.max_mutation_rate)
            self.members.append(seq)
        print(len(self.members))

    def get_apex(self):
        """ Returns the sequence posessing the highest fitness in this
        generation."""

        highest_fitness = 0
        apex = self.members[0]
        for seq in self.members:
            if seq.fitness > highest_fitness:
                apex = seq
                highest_fitness = seq.fitness
        return apex

    def get_average_fitness(self):
        """ Returns the average fitness value of this generation."""

        fitnesses_sum = 0
        for seq in self.members:
            fitnesses_sum += seq.fitness
        return fitnesses_sum / self.seqs_per_gen

    def get_next_generation_members(self):
        """ Returns a list containing the members of the next generation."""

        from math import ceil

        members = sorted(self.members, key=lambda x: x.fitness, reverse=True)
        n_to_breed = ceil(self.breed_rate * self.seqs_per_gen)
        n_copies_each = int(1 / self.breed_rate)

        next_generation_members = []        
        for seq in members[:n_to_breed]:
            for i in range(n_copies_each):
                next_generation_members.append(seq.get_mutated())
        return next_generation_members

    def get_next_generation(self):
        """ Returns the child generation of this generation."""

        next_generation = Generation(self.genome,
                                    self.heuristic,
                                    self.seqs_per_gen,
                                    self.breed_rate,
                                    self.max_mutation_rate)
        next_generation.members = self.get_next_generation_members()
        return next_generation