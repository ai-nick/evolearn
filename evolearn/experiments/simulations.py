
########################################################
#   ____  _      ___   _     ____   __    ___   _      #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ |  #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \|  #
#                                                      #
#                  Chad Carlson - 2017                 #
########################################################


from evolearn import algorithms
from evolearn import environments

from evolearn.utils.visualize import VisualizeLeader, Animation

import MultiNEAT as mneat
from copy import copy


class SimulationNEAT:

    """SimulationNEAT Experiment Simulation Class.
    
    Allows user to initialize a NEAT simulation of different 'flavors'.

    :param parameter_values: experiment Parameters object.
    
    """
    def __init__(self, parameters):

        # -------------------- ENVIRONMENT --------------------

        # Construct the environment the population will be evaluated on

        self.env_type = parameters.values['environment_type']
        self.env = self.construct_environment()

        # -------------------- SIMULATION --------------------

        # Population parameters

        self.num_inputs = self.env.observation_space
        self.num_outputs = self.env.action_space
        self.population_size = parameters.values['population_size']

        # Simulation parameters

        self.max_evaluations = parameters.values['max_evaluations']
        self.num_generations = parameters.values['num_generations']
        self.num_repetitions = parameters.values['num_repetitions']

        # Repetition and Generation verbose

        self.verbose = parameters.values['verbose']

        # Performance Plotting

        self.performance_plotting = parameters.values['performance_plotting']

        # Visualizing Leader Agent Networks at End of Simulation

        self.visualize_leader = parameters.values['visualize_leader']

        # Animating Leader Agent Behavior at End of Simulation

        self.animate_leader = parameters.values['animate_leader']
        self.leader_world = {}
        self.agent_value = self.env.agent_value

        # -------------------- ALGORITHM --------------------

        # Define the type of experiment (flavor) you are running

        self.neat_flavor = parameters.values['neat_flavor']

        # Define the algorithm to fit that flavor

        self.alg = self.construct_neat_flavor()

    def build_phenotype(self, current_genome):

        """
        Constructs an agent phenotype from its genotype.

        :param current_genome: agent genome.
        :return: agent phenotype network.
        """

        net = mneat.NeuralNetwork()
        current_genome.BuildPhenotype(net)

        return net

    def construct_environment(self):

        """
        Construct an Environment object from environment_type string.
        
        :return: Environment object instance. 
        """

        return getattr(environments, self.env_type)()

    def construct_neat_flavor(self):

        """
        Construct NEAT Algorithm object from neat_flavor string.
        
        :return: NEAT Algorithm object instance.
        """

        return getattr(algorithms, self.neat_flavor)(self.population_size, self.num_inputs, self.num_outputs, self.env, self.max_evaluations)

    def evaluate_agent_for_visualization(self, net, test_evaluations):

        """
        Evaluate a single agent phenotype on the current environment specifically for visualization

        :param current_genome: current agent genome
        :return: performance measure
        
        Todo:
            * This should also be moved to the NEAT module
        """

        # -------------------- ENVIRONMENT --------------------

        # Reset environment and retrieve initial observation

        observation = self.env.reset()

        # -------------------- EVALUATE AGENT --------------------

        # Initialize evaluation loop variables

        collide, evaluation, fitness = False, 0, 0

        # Main Evaluation Loop

        while (not collide) and (evaluation < test_evaluations):

            # Build visualization array for current evaluation

            self.leader_world[evaluation] = copy(self.env.world)

            # Place the agent into current visualization array

            self.leader_world[evaluation][self.env.agent.location[0], self.env.agent.location[1]] = self.agent_value

            # Single evaluation on current input

            output = self.alg.single_evaluation(net, observation)

            # Convert network output into relevant action in the environment

            action = self.env.reformat_action(output)

            # Return resulting observation, state and collide catch

            observation, state, collide = self.env.step(action)

            # Performance Update

            fitness += state

            # Evaluation Loop Step

            evaluation += 1

        return fitness

    def run(self):

        self.alg.run(self.num_repetitions, self.num_generations, self.verbose, self.performance_plotting)
