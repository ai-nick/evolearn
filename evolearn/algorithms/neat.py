
########################################################
#   ____  _      ___   _     ____   __    ___   _      #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ |  #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \|  #
#                                                      #
#                  Chad Carlson - 2017                 #
########################################################


import MultiNEAT as mneat


class NEAT:

    """NeuroEvolution of Augmenting Topologies (NEAT) Population Class.

    :param population_size: number of agents in the current simulation's population.
    :type population_size: int
    
    :param num_inputs: environment observation space.
    :type num_inputs: int
    
    :param num_outputs: environment action space.
    :type num_outputs: int

    """

    def __init__(self, population_size, num_inputs, num_outputs):

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

    def single_evaluation(self, net, current_input):

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
