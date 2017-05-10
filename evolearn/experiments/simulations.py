
#######################################################
#   ____  _      ___   _     ____   __    ___   _     #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ | #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \| #
#                                                     #
#                  Chad Carlson - 2017                #
#######################################################


from evolearn.algorithms import neat
from evolearn.environments import environment_simple
# from evolearn.utils.visualize import VisualizeLeader
import MultiNEAT as mneat
import numpy as np


class SimulationNEAT:

    """SimulationNEAT Experiment Simulation Class.
    
    Allows user to initialize a NEAT simulation of different 'flavors'.

    :param neat_flavor: NEAT experiment type; direct v. indirect encoding. Options: 'NEAT', 'HyperNEAT', 'ES-HyperNEAT'.
    :type neat_flavor: string
    
    :param environment_type: Options: 'SimpleEnvironment'. (Default='SimpleEnvironment')
    :type environment_type: string

    :param population_size: number of agents in experiment population. (Default=300)
    :type population_size: int
    
    :param max_evaluations: number of maximum evaluations/decisions an agent can have with the environment. (Default=100)
    :type max_evaluations: int
    
    :param num_generations: number of generations of evolution in experiment. (Default=300)
    :type : int
    
    :param num_repetitions: number of times entire experiment is replicated in a simulation. (Default=1)
    :type : int
    
    :param verbose: option for Generation and Repetition print strings during a simulation. (Default=False)
    :type verbose: bool
    
    :param performance_plotting: option to generate performance plots across simulation. (Default=False)
    :type performance_plotting: bool
    
    :param visualize_leader:
    :type visualize_leader: bool
    
    """

    def __init__(self, neat_flavor='NEAT', environment_type='SimpleEnvironment',
                 population_size=300, max_evaluations=100, num_generations=300,
                 num_repetitions=1, verbose=False, performance_plotting=False,
                 visualize_leader=False):

        # -------------------- CONSTANTS --------------------

        # constants_file.txt?
        # Ability to load and read from a constants file for experiment reproduction?

        # -------------------- ENVIRONMENT --------------------

        # Construct the environment the population will be evaluated on

        self.env_type = environment_type
        self.env = self.define_environment()

        # -------------------- SIMULATION --------------------

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

        self.visualizeLeader = visualize_leader

        # -------------------- ALGORITHM --------------------

        # Define the type of experiment (flavor) you are running

        self.NEAT_flavor = neat_flavor

        # Define the algorithm to fit that flavor

        self.alg = self.define_NEAT_flavor()

    def build_phenotype(self, current_genome):

        """
        Constructs an agent phenotype from its genotype.
        
        :param current_genome: agent genome.
        :return: agent phenotype network.
        """

        net = mneat.NeuralNetwork()
        current_genome.BuildPhenotype(net)

        return net

    def define_environment(self):

        '''Convert environment type string into an Environment object.

        :return: Environment object instance.
        '''

        return getattr(environment_simple, self.env_type)()

    def define_NEAT_flavor(self):

        '''Convert NEAT flavor string into NEAT experiment object.

        :return: NEAT experiment object instance.
        '''

        return getattr(neat, self.NEAT_flavor)(self.population_size, self.num_inputs, self.num_outputs)

    def evaluate(self, current_genome):

        '''
        Evaluate a single agent phenotype on the task.
        '''

        # Initialize fitness

        fitness = 0

        # Reset agent and environment

        self.env.reset()

        # Retrieve initial observation from the environment

        # observation = self.env.observation
        current_input = np.append( np.random.rand(self.num_inputs - 1,), 1.0 )

        # Build the agent phenotype

        net = self.build_phenotype(current_genome)

        # Main Evaluation Loop

        collide, evaluation = False, 0

        while (not collide) and (evaluation < self.max_evaluations):

            # Single evaluation on current input

            output = self.alg.single_evaluation(net, current_input)

            # Convert network output into relevant action in the environment

            action = self.env.reformat_action(output)

            # Return resulting observation, state and collide catch

            observation, state, collide = self.env.step( action )

            # Performance Update

            fitness += state

            # Evaluation Loop Step

            evaluation += 1

        return fitness

    def run(self):

        """
        Main simulation function.
        """

        # -------------------- MAIN EXPERIMENT --------------------

        # Main repetition loop

        for repetition in range(self.num_repetitions):

            # Main generation loop

            if self.verbose:

                print '- Repetition %d:' % (repetition + 1)

            for generation in range(self.num_generations):

                if self.verbose:

                    print '     - Generation %d:' % (generation + 1)

                # Perform a single generation

                self.single_generation()

        # -------------------- LEADER VISUALIZATION --------------------

        # if self.visualizeLeader:
        #
        #     if self.verbose:
        #         'Visualizing Best Performing Agent...'
        #
        #     VisualizeLeader(self.alg, self.num_inputs, self.num_outputs, self.NEAT_flavor)




    def single_generation(self):

        """
        Single generation of evaluation for a population on an environment. 
        
        :return: performance measure (i.e. fitness).
        """

        # Retrieve a list of all genomes in the population

        genome_list = mneat.GetGenomeList(self.alg.pop)

        # Main Population Evaluation Loop

        for current_genome in genome_list:

            # Evaluate the current genome

            fitness = self.evaluate(current_genome)

            # Reset the current genome's fitness

            current_genome.SetFitness(fitness)

        # Call a new Epoch - runs mutations and crossover, creating the next generation of genomes

        self.alg.pop.Epoch()





