
########################################################
#   ____  _      ___   _     ____   __    ___   _      #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ |  #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \|  #
#                                                      #
#                  Chad Carlson - 2017                 #
########################################################


from evolearn.algorithms import neat
from evolearn.environments import environment_simple
from evolearn.utils.visualize import VisualizeLeader, Animation

import MultiNEAT as mneat
from copy import copy
import numpy as np


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

        return getattr(environment_simple, self.env_type)()

    def construct_neat_flavor(self):

        """
        Construct NEAT Algorithm object from neat_flavor string.
        
        :return: NEAT Algorithm object instance.
        """

        return getattr(neat, self.neat_flavor)(self.population_size, self.num_inputs, self.num_outputs)

    def evaluate_agent(self, current_genome):

        """
        Evaluate a single agent phenotype on the current environment.
        
        :param current_genome: current agent genome
        :return: performance measure
        """

        # -------------------- ENVIRONMENT --------------------

        # Reset environment and retrieve initial observation

        observation = self.env.reset()

        # -------------------- AGENT --------------------

        # Build the agent phenotype

        net = self.build_phenotype(current_genome)

        # -------------------- EVALUATE AGENT --------------------

        # Initialize evaluation loop variables

        collide, evaluation, fitness = False, 0, 0

        # Main Evaluation Loop

        while (not collide) and (evaluation < self.max_evaluations):

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

    def evaluate_agent_for_visualization(self, net, test_evaluations):

        """
        Evaluate a single agent phenotype on the current environment specifically for visualization

        :param current_genome: current agent genome
        :return: performance measure
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

        """
        Main simulation function.
        """

        # -------------------- MAIN EXPERIMENT --------------------

        # Main Repetition Loop

        for repetition in range(self.num_repetitions):

            if self.verbose:

                print '\n- Repetition %d:' % (repetition + 1)

            # Main Generation Loop

            for generation in range(self.num_generations):

                if self.verbose:

                    print '     * Generation %d of %d:' % (generation + 1, self.num_generations)

                # Perform a single generation

                self.single_generation()

                if self.verbose:

                    print '         > Species: ', self.alg.pop.Species

        # -------------------- LEADER VISUALIZATION --------------------

        if self.visualize_leader:

            if self.verbose:

                print '\n- Visualizing Best Performing Agent...'

            VisualizeLeader(self.alg, self.num_inputs, self.num_outputs, self.neat_flavor)

        # -------------------- LEADER ANIMATION --------------------

        if self.animate_leader:

            if self.verbose:

                print '\n- Animating Best Performing Agent...'

            # Pull out the Best Performer (Leader) Genotype and build its Phenotype

            net = mneat.NeuralNetwork()
            self.alg.pop.Species[0].GetLeader().BuildPhenotype(net)

            if self.verbose:

                print '     * Species best performer Fitness in New Simulation:', self.evaluate_agent_for_visualization(net, 10 * self.max_evaluations)

            # Animate the thing

            leader_viz = Animation(self.leader_world)
            leader_viz.animate()

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

            fitness = self.evaluate_agent(current_genome)

            # Reset the current genome's fitness

            current_genome.SetFitness(fitness)

        # Call a new Epoch - runs mutation and crossover, creating offspring

        self.alg.pop.Epoch()
