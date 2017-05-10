
#######################################################
#   ____  _      ___   _     ____   __    ___   _     #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ | #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \| #
#                                                     #
#                  Chad Carlson - 2017                #
#######################################################


from evolearn.algorithms.neat import NEAT
from evolearn.environments.environment import SimpleEnvironment
from evolearn.utils.visualize import VisualizeLeader

import MultiNEAT as mneat
import numpy as np


class SimulationNEAT:

    """SimulationNEAT Experiment Simulation Class.
    
    Allows user to initialize a NEAT simulation of different 'flavors'.

    :param flavor: NEAT experiment type; direct v. indirect encoding. Options: 'NEAT', 'HyperNEAT', 'ES-HyperNEAT'.
    :type flavor: string

    """

    def __init__(self, NEAT_flavor='NEAT', environment='SimpleEnvironment', population_size=300,
                 max_evaluations=100, num_generations=300, num_repetitions=1, verbose=False, performance_plotting=False, visualizeLeader=False):

        # constants_file.txt?
        # Ability to load and read from a constants file for experiment reproduction?

        ############### ENVIRONMENT ###############

        # Define the environment the population with be evaluated on
        self.env_type = environment

        # Define an Environment class based on the type
        self.env = self.define_environment()

        ############### SIMULATION ###############

        # Population parameters
        self.num_inputs = self.env.observation_space
        self.num_outputs = self.env.action_space
        self.population_size = population_size

        # Simulation parameters
        self.max_evaluations = max_evaluations

        self.num_generations = num_generations
        self.num_repetitions = num_repetitions

        # Repetition and Generation verbose
        self.verbose = verbose

        # Performance Plotting
        self.performance_plotting = performance_plotting

        # Visualizing Leader Agent Networks at End of Simulation
        self.visualizeLeader = visualizeLeader

        ############### ALGORITHM ###############

        # Define the type of experiment (flavor) you are running
        self.NEAT_flavor = NEAT_flavor

        # Define the algorithm to fit that flavor
        self.alg = self.define_NEAT_flavor()

    def define_NEAT_flavor(self):

        '''Convert NEAT flavor string into NEAT experiment object.
        
        :return: NEAT experiment object instance.
        '''

        if self.NEAT_flavor == 'NEAT':
            alg = NEAT(self.population_size, self.num_inputs, self.num_outputs)

        return alg

    def define_environment(self):

        '''Convert environment type string into an Environment object.

        :return: Environment object instance.
        '''

        if self.env_type == 'SimpleEnvironment':
            environment = SimpleEnvironment()

        return environment


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

        if self.visualizeLeader:

            if self.verbose:
                'Visualizing Best Performing Agent...'

            VisualizeLeader(self.alg, self.num_inputs, self.num_outputs, self.NEAT_flavor)


    def single_generation(self):

        '''
        Single Generation of a Population on the Task.
        
        :return: performance measure (i.e. fitness).
        '''

        # Retrieve a list of all genomes in the population
        genome_list = mneat.GetGenomeList(self.alg.pop)

        for current_genome in genome_list:

            # Evaluate the current genome

            fitness = self.evaluate(current_genome)

            # fitness = self.alg.pop_evaluate(current_genome)

            # Reset the current genome's fitness
            current_genome.SetFitness(fitness)

        self.alg.pop.Epoch()


    def evaluate(self, current_genome):

        '''
        Evaluate a single agent phenotype on the task.
        '''

        # Initialize fitness to keep track for update
        fitness = 0

        # RESET THE AGENT & ENVIRONMENT
        self.env.reset()
        # # Get the initial input
        # current_input = self.env.observation

        # Construct a DUMMY INPUT - replace with call to environment initial observation
        current_input = np.append( np.random.rand(self.num_inputs - 1,), 1.0 )

        # Build the neural network phenotype from the cppn genotype
        net = mneat.NeuralNetwork()
        current_genome.BuildPhenotype(net)

        # # Construct a DUMMY INPUT - replace with call to environment initial observation
        # current_input = np.append( np.random.rand(self.num_inputs - 1,), 1.0 )

        # Evaluation loop - allow for 'quit simulation' bool catch to exit while loop
        collide, evaluation = 0, 0
        while (not collide) and (evaluation < self.max_evaluations):
        # for evaluation in range(self.max_evaluations):

            # MAKE AN ACTION ON THE ENVIRONMENT WRT CURRENT LOCATION INPUT

            # Agent makes a single evaluation on the current_input
            output = self.alg.single_evaluation(net, current_input)

            # Convert network output into relevant action in environment, return next observation, state and break catch
            observation, state, collide = self.env.step( self.env.reformat_action(output) )

            # Dummy fitness update - replaced with environment call/state
            # reward = 1.0 - output[0]
            fitness += state

            evaluation += 1

        return fitness


