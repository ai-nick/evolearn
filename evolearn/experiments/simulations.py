
####################################
# ----------- evolearn ----------- #
####################################


from evolearn.algorithms.neat import NEAT


import MultiNEAT as mneat
import numpy as np


class SimulationNEAT:

    """SimulationNEAT Experiment Simulation Class.
    
    Allows user to initialize a NEAT simulation of different 'flavors'.

    :param flavor: NEAT experiment type; direct v. indirect encoding. Options: 'NEAT', 'HyperNEAT', 'ES-HyperNEAT'.
    :type flavor: string

    """

    def __init__(self, flavor='NEAT', population_size=300, max_evaluations=100, num_generations=300, num_repetitions=1, verbose=False, visualizeLeader=True):

        # constants_file.txt?
        # Ability to load and read from a constants file for experiment reproduction?

        # Population parameters
        self.num_inputs = 5
        self.num_outputs = 1
        self.population_size = population_size

        # Simulation parameters
        self.max_evaluations = max_evaluations

        self.num_generations = num_generations
        self.num_repetitions = num_repetitions

        # Repetition and Generation verbose
        self.verbose = verbose

        # Visualizing Leader Agent at End of Simulation
        self.visualizeLeader = visualizeLeader

        # Define the type of experiment you are running
        self.flavor = flavor

        # Define the algorithm to fit that flavor
        self.alg = self.select_flavor()

        # Define the environment the population with be evaluated on
        self.env = []

    def select_flavor(self):

        '''Convert NEAT flavor string into NEAT experiment object.
        
        :param flavor: NEAT experiment type; direct v. indirect encoding. Options: 'NEAT', 'HyperNEAT', 'ES-HyperNEAT'.
        :type flavor: string
        :return: NEAT experiment object instance.
        '''

        if self.flavor == 'NEAT':
            alg = NEAT(self.population_size, self.num_inputs, self.num_outputs, self.max_evaluations)

        return alg

    def run(self):

        '''
        Main simulation function.
        '''

        for repetition in range(self.num_repetitions):

            # Should be able to keep this repetition verbose, but I think there is a generation
            # verbose built in to be called/passed to

            if self.verbose:
                print '- Repetition %d:' % (repetition + 1)

            for generation in range(self.num_generations):

                if self.verbose:
                    print '     - Generation %d:' % (generation + 1)

                self.single_generation()


    def single_generation(self):

        '''
        Single Generation of a Population on the Task.
        '''

        # Retrieve a list of all genomes in the population
        genome_list = mneat.GetGenomeList(self.alg.pop)

        for current_genome in genome_list:

            # Evaluate the current genome

            # fitness = self.evaluate(current_genome)

            fitness = self.alg.pop_evaluate(current_genome)

            # Reset the current genome's fitness
            current_genome.SetFitness(fitness)

        self.alg.pop.Epoch()




    # def evaluate(self, current_genome):
    #
    #     '''
    #     Evaluate a single agent phenotype on the task.
    #     '''
    #
    #     # Initialize fitness to keep track for update
    #     fitness = 0
    #
    #     # Build the neural network phenotype from the cppn genotype
    #     net = mneat.NeuralNetwork()
    #     current_genome.BuildPhenotype(net)
    #
    #     # Construct a DUMMY INPUT - replace with call to environment initial observation
    #     current_input = np.append( np.random.rand(self.num_inputs - 1,), 1.0 )
    #
    #     # Evaluation loop - allow for 'quit simulation' bool catch to exit while loop
    #     for evaluation in range(self.max_evaluations):
    #
    #         # Agent makes a single evaluation on the current_input
    #         output, current_input = self.alg.single_evaluation(net, current_input)
    #
    #         # Dummy fitness update - replaced with environment call/state
    #         reward = 1.0 - output[0]
    #         fitness += reward
    #
    #     return fitness
    #

