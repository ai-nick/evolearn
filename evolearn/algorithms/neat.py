
####################################
# ----------- evolearn ----------- #
####################################


import MultiNEAT as mneat
import numpy as np


class NEAT:

    """NEAT test class

    :param genome: population of cppn networks.
    :type genome: NaN

    """

    def __init__(self, PopulationSize, num_inputs, num_outputs, max_evaluations):

        # Define the NEAT parameters
        self.params = mneat.Parameters()

        self.params.PopulationSize = PopulationSize

        # Define the inputs, outputs of the neural network
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

        self.max_evaluations = max_evaluations

        # Define the genome
        self.genome = mneat.Genome(0, self.num_inputs, 0, self.num_outputs, False, mneat.ActivationFunction.UNSIGNED_SIGMOID,
                             mneat.ActivationFunction.UNSIGNED_SIGMOID, 0, self.params)

        # Define the population
        step = 0
        self.pop = mneat.Population(self.genome, self.params, True, 1.0, step)



    # def pop_single_generation(self):
    #
    #     '''
    #     Single Generation of a Population on the Task.
    #     '''
    #
    #     # Retrieve a list of all genomes in the population
    #     genome_list = mneat.GetGenomeList(self.pop)
    #
    #     for current_genome in genome_list:
    #
    #         # Evaluate the current genome
    #         # fitness = self.evaluate(current_genome)
    #
    #         fitness = self.pop_evaluate(current_genome)
    #
    #         # Reset the current genome's fitness
    #         current_genome.SetFitness(fitness)
    #
    #     self.pop.Epoch()




    def pop_evaluate(self, current_genome):

        '''
        Evaluate a single agent phenotype on the task.
        '''

        # Initialize fitness to keep track for update
        fitness = 0

        # Build the neural network phenotype from the cppn genotype
        net = mneat.NeuralNetwork()
        current_genome.BuildPhenotype(net)

        # Construct a dummy input - replace with call to environment initial observation
        current_input = np.append( np.random.rand(self.num_inputs - 1,), 1.0 )

        # Evaluation loop - allow for 'quit simulation' bool catch to exit while loop
        for evaluation in range(self.max_evaluations):

            # Agent makes a single evaluation on the current_input
            output, current_input = self.single_evaluation(net, current_input)

            # Dummy fitness update - replaced with environment call/state
            reward = 1.0 - output[0]
            fitness += reward

        return fitness



    def single_evaluation(self, net, current_input):

        net.Input(current_input)
        net.Activate()
        output = net.Output()

        new_observation = current_input

        return output, new_observation







    # def evaluate(self, current_genome, current_input):
    #
    #     # Build the neural network phenotype from the cppn genotype
    #     net = mneat.NeuralNetwork()
    #     current_genome.BuildPhenotype(net)
    #
    #     # let's input just one pattern to the net, activate it once and get the output
    #     # current_input = [1.0, 0.0, 1.0]
    #     net.Input(current_input)
    #     net.Activate()
    #     output = net.Output()
    #
    #     # the output can be used as any other Python iterable. For the purposes of the tutorial, we will consider the fitness of the individual
    #     # to be the neural network that outputs constantly 0.0 from the first output (the second output is ignored)
    #
    #     fitness = 1.0 - output[0]
    #     return fitness, output
    #
    # def single_generation(self):
    #
    #     # retrieve a list of all genomes in the population
    #     genome_list = mneat.GetGenomeList(self.pop)
    #
    #     # apply the evaluation function to all genomes
    #
    #     current_input = [1.0, 0.0, 1.0]
    #
    #     for current_genome in genome_list:
    #         fitness, output = self.evaluate(current_genome, current_input)
    #         current_genome.SetFitness(fitness)
    #
    #         # at this point we may output some information regarding the progress of evolution, best fitness, etc. it's also
    #         # the place to put any code that tracks the progress and saves the best genome or the entire population.
    #
    #     # advance to the next generation
    #     self.pop.Epoch()
    #
    # def run(self):
    #
    #     for generation in range(self.num_generations):
    #
    #         # if self.verbose:
    #         #     print '- Generation', generation
    #
    #         self.single_generation()
