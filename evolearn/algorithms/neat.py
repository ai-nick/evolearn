
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
import matplotlib.pyplot as plt
import time

class ESHyperNEAT:

    def __init__(self):
        pass

class HyperNEAT:

    """
    Hypercube-based NeuroEvolution of Augmenting Topologies (NEAT) Population Class.
    
    """

    def __init__(self, population_size, num_inputs, num_outputs, environment, max_evaluations):

        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

        self.env = environment
        self.max_evaluations = max_evaluations

        self.substrate_type = 'simple'
        sub = Substrate(self.substrate_type)
        # print sub.substrate
        # unpacking this is odd - is there a way to make this more systematic?
        self.substrate = mneat.Substrate(sub.substrate[0], sub.substrate[1], sub.substrate[2])

        self.substrate.m_allow_output_hidden_links = False
        self.substrate.m_allow_output_output_links = False
        self.substrate.m_allow_looped_hidden_links = False
        self.substrate.m_allow_looped_output_links = False
        #
        self.substrate.m_allow_input_hidden_links = True
        self.substrate.m_allow_input_output_links = False
        self.substrate.m_allow_hidden_output_links = True
        self.substrate.m_allow_hidden_hidden_links = False
        #
        self.substrate.m_hidden_nodes_activation = mneat.ActivationFunction.SIGNED_SIGMOID
        self.substrate.m_output_nodes_activation = mneat.ActivationFunction.UNSIGNED_SIGMOID
        #
        self.substrate.m_with_distance = True
        #
        self.substrate.m_max_weight_and_bias = 8.0

        self.params = mneat.Parameters()

        self.params.PopulationSize = population_size

        self.params.DynamicCompatibility = True
        self.params.CompatTreshold = 2.0
        self.params.YoungAgeTreshold = 15
        self.params.SpeciesMaxStagnation = 100
        self.params.OldAgeTreshold = 35
        self.params.MinSpecies = 5
        self.params.MaxSpecies = 10
        self.params.RouletteWheelSelection = False

        self.params.MutateRemLinkProb = 0.02
        self.params.RecurrentProb = 0
        self.params.OverallMutationRate = 0.15
        self.params.MutateAddLinkProb = 0.08
        self.params.MutateAddNeuronProb = 0.01
        self.params.MutateWeightsProb = 0.90
        self.params.MaxWeight = 8.0
        self.params.WeightMutationMaxPower = 0.2
        self.params.WeightReplacementMaxPower = 1.0

        self.params.MutateActivationAProb = 0.0
        self.params.ActivationAMutationMaxPower = 0.5
        self.params.MinActivationA = 0.05
        self.params.MaxActivationA = 6.0

        self.params.MutateNeuronActivationTypeProb = 0.03

        self.params.ActivationFunction_SignedSigmoid_Prob = 0.0
        self.params.ActivationFunction_UnsignedSigmoid_Prob = 0.0
        self.params.ActivationFunction_Tanh_Prob = 1.0
        self.params.ActivationFunction_TanhCubic_Prob = 0.0
        self.params.ActivationFunction_SignedStep_Prob = 1.0
        self.params.ActivationFunction_UnsignedStep_Prob = 0.0
        self.params.ActivationFunction_SignedGauss_Prob = 1.0
        self.params.ActivationFunction_UnsignedGauss_Prob = 0.0
        self.params.ActivationFunction_Abs_Prob = 0.0
        self.params.ActivationFunction_SignedSine_Prob = 1.0
        self.params.ActivationFunction_UnsignedSine_Prob = 0.0
        self.params.ActivationFunction_Linear_Prob = 1.0

        self.params.AllowLoops = False

        self.genome = mneat.Genome(0, self.substrate.GetMinCPPNInputs(), 0, self.substrate.GetMinCPPNOutputs(), False,
                                   mneat.ActivationFunction.TANH, mneat.ActivationFunction.TANH, 0, self.params)

        run = 0
        self.pop = mneat.Population(self.genome, self.params, True, 1.0, run)

    def build_phenotype(self, current_genome):

        """
        Constructs an agent phenotype from its genotype.

        :param current_genome: agent genome.
        :return: agent phenotype network.
        """

        net = mneat.NeuralNetwork()
        current_genome.BuildHyperNEATPhenotype(net, self.substrate)

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

        # Clear any previous activations

        net.Flush()

        # Activate the network and find its output

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

        stats = {'Min': min_fitness, 'Max': max_fitness, 'Mean': avg_fitness, 'STD': dev}

        species_leaders = [self.pop.Species[species].GetLeader() for species in range(len(self.pop.Species))]

        # Call a new Epoch - runs mutation and crossover, creating offspring for next generation

        self.pop.Epoch()

        return stats, species_leaders

    def run(self, num_repetitions, num_generations, verbose, performance_plotting):

        """
        Main simulation function.
        """

        # -------------------- MAIN EXPERIMENT --------------------

        # Main Repetition Loop

        for repetition in range(num_repetitions):

            if verbose:
                print '\n- Repetition %d:' % (repetition + 1)

            # Main Generation Loop

            max = np.zeros((num_generations,))
            min = np.zeros((num_generations,))
            avg = np.zeros((num_generations,))
            dev = np.zeros((num_generations,))
            num_species = np.zeros((num_generations,))

            # Define a Population for the current repetition

            self.pop = mneat.Population(self.genome, self.params, True, 1.0, repetition)
            self.pop.RNG.Seed(int(time.clock())*100)

            for generation in range(num_generations):

                if verbose:
                    print '\n     * Generation %d of %d:' % (generation + 1, num_generations)

                # Perform a single generation on the population

                stats, species_leaders = self.single_generation()

                # Place stats into their correct arrays

                max[generation], min[generation], avg[generation], dev[generation], num_species[generation] = \
                    stats['Max'], stats['Min'], stats['Mean'], stats['STD'], len(species_leaders)

                if verbose:
                    print '         > Generation Stats:', stats
                    print '         > Species Leaders:', species_leaders

                    #
                    #
                    # -------------------- PERFORMANCE PLOTTING --------------------
                    # It would be better if these were placed into parameters of a 'Results' Object, which could then be passed to Visualize and Animate
                    # It would make this module much less messy, save variable inputs for run function, and allow Results to be built for whichever flavor
                    #   of NEAT is currently in use.

            if performance_plotting:
                x = range(num_generations)

                plt.subplot(1, num_repetitions, repetition + 1)
                # plt.errorbar(x, avg, yerr=dev)
                plt.plot(x, avg, 'g', label='Average Fit')
                plt.plot(x, min, 'b', label='Min Fit')
                plt.plot(x, max, 'r', label='Max Fit')
                plt.plot(x, num_species, 'k', label='Number of Species')

                density = self.env.nutrient_density * 100

                title = 'Nut Density %:' + str(density) + ', Variable Nut: ' + str(
                    self.env.variable_nutrients) + ', Pop Size:' + str(
                    self.params.PopulationSize) + ', Max Evals:' + str(self.max_evaluations) + ', Num Gens:' + str(
                    num_generations)

                plt.title(title)
                plt.legend(loc='upper left')
                plt.xlabel('Generation')
                plt.ylabel('Performance/Fitness')

        if performance_plotting:
            # In the case of many repetitions, the plots should be a choice of averages between runs or specific runs
            plt.show()

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

        # Clear any previous activations

        net.Flush()

        # Activate the network and find its output

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

    def run(self, num_repetitions, num_generations, verbose, performance_plotting):

        """
        Main simulation function.
        """

        # -------------------- MAIN EXPERIMENT --------------------

        # Main Repetition Loop

        for repetition in range(num_repetitions):

            if verbose:

                print '\n- Repetition %d:' % (repetition + 1)

            # Main Generation Loop

            max = np.zeros((num_generations, ))
            min = np.zeros((num_generations, ))
            avg = np.zeros((num_generations, ))
            dev = np.zeros((num_generations, ))
            num_species = np.zeros((num_generations, ))

            # Define a Population for the current repetition

            self.pop = mneat.Population(self.genome, self.params, True, 1.0, repetition)

            for generation in range(num_generations):

                if verbose:

                    print '\n     * Generation %d of %d:' % (generation + 1, num_generations)


                # Perform a single generation on the population

                stats, species_leaders = self.single_generation()

                # Place stats into their correct arrays

                max[generation], min[generation], avg[generation], dev[generation], num_species[generation] = stats['Max'], stats['Min'], stats['Mean'], stats['STD'], len(species_leaders)

                if verbose:

                    print '         > Generation Stats:', stats
                    print '         > Species Leaders:', species_leaders

        #
        #
        # -------------------- PERFORMANCE PLOTTING --------------------
        # It would be better if these were placed into parameters of a 'Results' Object, which could then be passed to Visualize and Animate
        # It would make this module much less messy, save variable inputs for run function, and allow Results to be built for whichever flavor
        #   of NEAT is currently in use.

            if performance_plotting:

                x = range(num_generations)

                plt.subplot(1, num_repetitions, repetition + 1)
                # plt.errorbar(x, avg, yerr=dev)
                plt.plot(x, avg, 'g', label='Average Fit')
                plt.plot(x, min, 'b', label='Min Fit')
                plt.plot(x, max, 'r', label='Max Fit')
                plt.plot(x, num_species, 'k', label='Number of Species')

                density = self.env.nutrient_density * 100

                title = 'Nut Density %:' + str(density) + ', Variable Nut: ' + str(self.env.variable_nutrients) +', Pop Size:' + str(self.params.PopulationSize) + ', Max Evals:' + str(self.max_evaluations) + ', Num Gens:' + str(num_generations)

                plt.title(title)
                plt.legend(loc='upper left')
                plt.xlabel('Generation')
                plt.ylabel('Performance/Fitness')

        if performance_plotting:
            # In the case of many repetitions, the plots should be a choice of averages between runs or specific runs
            plt.show()
        #
        # # -------------------- LEADER VISUALIZATION --------------------
        #
        # if self.visualize_leader:
        #
        #     if self.verbose:
        #
        #         print '\n- Visualizing Best Performing Agent...'
        #
        #     VisualizeLeader(self.alg, self.num_inputs, self.num_outputs, self.neat_flavor)
        #
        # # -------------------- LEADER ANIMATION --------------------
        #
        # if self.animate_leader:
        #
        #     if self.verbose:
        #
        #         print '\n- Animating Best Performing Agent...'
        #
        #     # Pull out the Best Performer (Leader) Genotype and build its Phenotype
        #
        #     net = mneat.NeuralNetwork()
        #     self.alg.pop.Species[0].GetLeader().BuildPhenotype(net)
        #
        #     if self.verbose:
        #
        #         print '     * Species best performer Fitness in New Simulation:', self.evaluate_agent_for_visualization(net, 20 * self.max_evaluations)
        #
        #
        #     # Animate the thing
        #
        #     leader_viz = Animation(self.leader_world)
        #     leader_viz.animate()

