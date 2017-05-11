
########################################################
#   ____  _      ___   _     ____   __    ___   _      #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ |  #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \|  #
#                                                      #
#                  Chad Carlson - 2017                 #
########################################################

from evolearn.algorithms.neat_substrates import Substrate

import MultiNEAT as mneat
import numpy as np


class ESHyperNEAT:

    def __init__(self):
        pass

class HyperNEAT:

    """
    Hypercube-based NeuroEvolution of Augmenting Topologies (NEAT) Population Class.
    
    """

    def __init__(self):

        self.substrate_type = 'simple'
        substrate_coords = Substrate(self.substrate_type)
        self.substrate = mneat.Substrate(substrate_coords[0])

class NEAT:

    """NeuroEvolution of Augmenting Topologies (NEAT) Population Class.

    :param population_size: number of agents in the current simulation's population.
    :type population_size: int
    
    :param num_inputs: environment observation space.
    :type num_inputs: int
    
    :param num_outputs: environment action space.
    :type num_outputs: int

    """

    def __init__(self, population_size, num_inputs, num_outputs, environment, max_evaluations):

        # Define the NEAT parameters
        self.params = mneat.Parameters()

        self.params.PopulationSize = population_size

        # Define the inputs, outputs of the neural network
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

        # Define the genome
        self.genome = mneat.Genome(0, self.num_inputs, 0, self.num_outputs, False, mneat.ActivationFunction.UNSIGNED_SIGMOID,
                                mneat.ActivationFunction.UNSIGNED_SIGMOID, 0, self.params)

        # Define the population
        step = 0
        self.pop = mneat.Population(self.genome, self.params, True, 1.0, step)

        self.env = environment
        self.max_evaluations = max_evaluations

    @staticmethod
    def build_phenotype(current_genome):

        """
        Constructs an agent phenotype from its genotype.

        :param current_genome: agent genome.
        :return: agent phenotype network.
        """

        net = mneat.NeuralNetwork()
        current_genome.BuildPhenotype(net)

        return net

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

            output = self.single_evaluation(net, observation)

            # Convert network output into relevant action in the environment

            action = self.env.reformat_action(output)

            # Return resulting observation, state and collide catch

            observation, state, collide = self.env.step(action)

            # Performance Update

            fitness += state

            # Evaluation Loop Step

            evaluation += 1

        return fitness

    @staticmethod
    def single_evaluation(net, current_input):

        """
        Evaluate agent phenotype network on current environment input.
        
        :param net: agent phenotype network.
        :param current_input: current environment observation.
        :return: network output
        """

        net.Input(current_input)
        net.Activate()
        output = net.Output()

        return output

    def single_generation(self):
        """
        Single generation of evaluation for a population on an environment. 

        :return: performance measure (i.e. fitness).
        """

        # Retrieve a list of all genomes in the population

        genome_list = mneat.GetGenomeList(self.pop)

        # Evaluate fitness for each genome in genome_list using MultiNEAT built-in

        fitness_list = mneat.EvaluateGenomeList_Serial(genome_list, self.evaluate_agent, display=False)

        # Attach the fitness_list to the genome_list

        mneat.ZipFitness(genome_list, fitness_list)

        # Set aside some stats for output

        population_fitness = [x.GetFitness() for x in mneat.GetGenomeList(self.pop)]

        max_fitness = max(population_fitness)
        min_fitness = min(population_fitness)
        avg_fitness = np.mean(population_fitness)
        dev = np.std(population_fitness)

        stats = { 'Min': min_fitness, 'Max': max_fitness, 'Mean': avg_fitness, 'STD': dev }

        species_leaders = [self.pop.Species[species].GetLeader() for species in range(len(self.pop.Species))]

        # Call a new Epoch - runs mutation and crossover, creating offspring for next generation

        self.pop.Epoch()

        return stats, species_leaders
