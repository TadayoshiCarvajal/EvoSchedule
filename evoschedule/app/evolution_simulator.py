class EvolutionSimulator:
    def __init__( self,
                  genome, 
                  heuristic,
                  n_generations = 200,
                  seqs_per_gen = 200,
                  breed_rate = .1,
                  max_mutation_rate = 0.01):
        """ An EvolutionSimulator is a simulation that runs a genetic algorithm
        for a specified number of generations, in the attempt to produce a high
        fitness schedule. Parameters such as n_generations, breed_rate, and 
        max_mutation_rate allow us to customize the evolution process.

        genome - Genome - containing information such as number of alleles, and genes
                          per gene type.
        heuristic - Heuristic - this object contains a function that provides the fitness.

        n_generations - int - the number of iterations for the main loop of the evolution
                              algorithm.
        seq_per_gen - int - the number of sequences in each generation.

        breed_rate - float - a percentage expressed as a float which determines what 
                             percent of the sequences breed into the next generation.
                             The top breed_rate % of sequences get to "breed".
        max_mutation_rate - float - a percentate which determines how many mutations
                             occur at most from parent sequences to child sequence."""
        from app.generation import Generation

        self.genome = genome
        self.heuristic = heuristic
        self.n_generations = n_generations
        self.seqs_per_gen = seqs_per_gen
        self.breed_rate = breed_rate
        self.max_mutation_rate = max_mutation_rate
        self.current_generation = Generation(genome, 
                                            heuristic, 
                                            seqs_per_gen, 
                                            breed_rate, 
                                            max_mutation_rate)

        self.current_generation.generate_members()
        self.evolution_apex = self.current_generation.get_apex()

        self.generational_average_fitness = []
        self.generation_apexes_fitness = []
        self.generational_evolution_apexes_fitness = []

    def run(self):
        """ Runs the genetic algorithm.
        
        The output of this is the best scoring sequence accross all generations."""
        from tqdm import tqdm
        
        for i in tqdm(range(self.n_generations)):
            # Get the generation data.
            generation_apex = self.current_generation.get_apex()
            average_fitness = self.current_generation.get_average_fitness()
            if generation_apex.fitness > self.evolution_apex.fitness:
                self.evolution_apex = generation_apex

            # Store generation data for evolution graph:
            self.generation_apexes_fitness.append(generation_apex.fitness)
            self.generational_evolution_apexes_fitness.append(self.evolution_apex.fitness)
            self.generational_average_fitness.append(average_fitness)

            # Update the generation
            self.current_generation = self.current_generation.get_next_generation()
        
        return self.evolution_apex

    def show_evolution_graph(self):
        """ Displays the data obtained from the evolution in a graph.
        
        4 pieces of information are displayed on the graph:
        
            1.  the average fitness of the generation.
            2.  the max fitness of the generation.
            3.  the best fitness discovered so far.
            4.  the highest possible fitness obtained by the 
                hungarian algorithm. (This is always 1.0)"""
        import matplotlib.pyplot as plt
        import numpy as np

        plt.plot(np.arange(self.n_generations), 
                            self.generational_average_fitness, 
                            color = "blue",
                            label = "Average")

        plt.plot(np.arange(self.n_generations), 
                            self.generation_apexes_fitness, 
                            color = "green",
                            label = "Apex")

        plt.plot(np.arange(self.n_generations), 
                            self.generational_evolution_apexes_fitness, 
                            color = "red", 
                            linestyle="--",
                            label = "Best Discovered Apex")
        plt.plot(np.arange(self.n_generations), 
                            [1.0]*self.n_generations,
                            color = "purple",
                            label = "Optimal Fitness")

        plt.title('Evolution Graph')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.legend(loc = "lower right")
        plt.show()