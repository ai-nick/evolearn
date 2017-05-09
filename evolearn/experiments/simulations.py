
from evolearn.algorithms.neat import NEAT


class SimulationNEAT:

    """SimulationNEAT Experiment Simulation Class.
    
    Allows user to initialize a NEAT simulation of different 'flavors'.

    :param flavor: NEAT experiment type; direct v. indirect encoding. Options: 'NEAT', 'HyperNEAT', 'ES-HyperNEAT'.
    :type flavor: string

    """

    def __init__(self, flavor='NEAT', population_size=300, max_evaluations=100, num_generations=300, num_repetitions=1, verbose=False):

        # constants_file.txt?
        # Ability to load and read from a constants file for experiment reproduction?

        # Simulation parameters
        self.population_size = population_size
        self.max_evaluations = max_evaluations

        self.num_generations = num_generations
        self.num_repetitions = num_repetitions

        # Repetition and Generation verbose
        self.verbose = verbose

        # Define the type of experiment you are running
        self.flavor = flavor

        # Define the algorithm to fit that flavor
        self.alg = self.select_flavor(self.flavor)

        # Define the environment the population with be evaluated on
        self.env = []

    def select_flavor(self, flavor):

        '''Convert NEAT flavor string into NEAT experiment object.
        
        :param flavor: NEAT experiment type; direct v. indirect encoding. Options: 'NEAT', 'HyperNEAT', 'ES-HyperNEAT'.
        :type flavor: string
        :return: NEAT experiment object instance.
        '''

        if flavor == 'NEAT':
            alg = NEAT(self.population_size)

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
        pass

    def evaluate(self):

        for evaluation in range(self.max_evaluations):

            self.alg.evaluate()

