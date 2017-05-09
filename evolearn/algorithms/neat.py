
import MultiNEAT as mneat


class NEAT:

    """NEAT test class

    :param genome: population of cppn networks.
    :type genome: NaN

    """

    def __init__(self, PopulationSize=300, verbose=False):

        # Define the NEAT parameters
        self.params = mneat.Parameters()

        self.params.PopulationSize = PopulationSize

        # Define the inputs, outputs of the neural network
        self.num_inputs = 5
        self.num_outputs = 1

        # Define the genome
        self.genome = mneat.Genome(0, self.num_inputs, 0, self.num_outputs, False, mneat.ActivationFunction.UNSIGNED_SIGMOID,
                             mneat.ActivationFunction.UNSIGNED_SIGMOID, 0, self.params)

        # Define the population
        step = 0
        self.pop = mneat.Population(self.genome, self.params, True, 1.0, step)

        # Simulation parameters
        self.num_generations = 500

        self.verbose = verbose

    def evaluate(self, current_genome, current_input):

        # Build the neural network phenotype from the cppn genotype
        net = mneat.NeuralNetwork()
        current_genome.BuildPhenotype(net)

        # let's input just one pattern to the net, activate it once and get the output
        # current_input = [1.0, 0.0, 1.0]
        net.Input(current_input)
        net.Activate()
        output = net.Output()

        # the output can be used as any other Python iterable. For the purposes of the tutorial, we will consider the fitness of the individual
        # to be the neural network that outputs constantly 0.0 from the first output (the second output is ignored)

        fitness = 1.0 - output[0]
        return fitness, output

    def single_generation(self):

        # retrieve a list of all genomes in the population
        genome_list = mneat.GetGenomeList(self.pop)

        # apply the evaluation function to all genomes

        current_input = [1.0, 0.0, 1.0]

        for current_genome in genome_list:
            fitness, output = self.evaluate(current_genome, current_input)
            current_genome.SetFitness(fitness)

            # at this point we may output some information regarding the progress of evolution, best fitness, etc. it's also
            # the place to put any code that tracks the progress and saves the best genome or the entire population.

        # advance to the next generation
        self.pop.Epoch()

    def run(self):

        for generation in range(self.num_generations):

            if self.verbose:
                print '- Generation', generation

            self.single_generation()
