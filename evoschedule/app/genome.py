class Genome:
    def __init__(self, time_scale, tasks, task_chunks, n_alleles, allele_size):
        """ An object which tells us information about what constitutes
        a valid sequence. A valid sequence will have the correct number of
        alleles and the correct quantity of genes per task."""
        
        self.time_scale = time_scale

        # The list of unique tasks
        self.tasks = tasks

        # The pairing of tasks and number of genes to place
        self.genes = task_chunks

        # The total number of time slots to fill
        self.n_alleles = n_alleles

        # The number of minutes each allele represents
        self.allele_size = allele_size

    def get_random_sequence(self):
        """ Uses the genome data to randomly generate a sequence."""

        from random import shuffle

        sequence = [None] * self.n_alleles

        i = 0
        for task in self.tasks:
            for j in range(self.genes[task]):
                sequence[i] = task
                i += 1
        shuffle(sequence)
        return sequence