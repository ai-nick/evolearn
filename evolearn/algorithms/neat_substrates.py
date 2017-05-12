
########################################################
#   ____  _      ___   _     ____   __    ___   _      #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ |  #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \|  #
#                                                      #
#                  Chad Carlson - 2017                 #
########################################################


import numpy as np
import itertools


class Substrate:

    """
    Substrate class for sampling potential phenotype node locations.
    """

    def __init__(self, substrate_type):

        self.substrate_type = substrate_type
        self.substrate_input, self.substrate_hidden, self.substrate_output = self.define_substrate()

    def define_substrate(self):

        '''
        Define substrate based on type.
        
        :return: substrate node positions: substrate_input, substrate_hidden, substrate_output
        '''

        substrate_input, substrate_hidden, substrate_output = 'unknown', 'unknown', 'unknown'

        if self.substrate_type == 'simple':

            # Simple substrate copied from TestHyperNEAT example in MultiNEAT/examples. (3 inputs, 3 (sic, noted as 2 in docs) hidden and 1 output)

            substrate_input = [(-1, -1), (-1, 0), (-1, 1)]
            substrate_hidden = [(0, -1), (0, 0), (0, 1)]
            substrate_output = [(1, 0)]

        elif self.substrate_type == '5x5':

            # 5x5 substrate

            substrate_input, substrate_hidden, substrate_output = self.construct_node_positions(5)

        elif self.substrate_type == '10x10':

            # 10x10 substrate

            substrate_input, substrate_hidden, substrate_output = self.construct_node_positions(10)

        elif self.substrate_type == '25x25':

            # 25x25 substrate

            substrate_input, substrate_hidden, substrate_output = self.construct_node_positions(25)

        elif self.substrate_type == '100x100':

            # 100x100 substrate

            substrate_input, substrate_hidden, substrate_output = self.construct_node_positions(100)

        elif self.substrate_type == 'ES':
            pass

        return substrate_input, substrate_hidden, substrate_output

    def construct_node_positions(self, resolution):

        '''
        Define substrate node positions using a meshgrid.
        
        :param resolution: number of nodes in each row and column (resolution ** 2 total nodes)
        :return: substrate_input, substrate_hidden, substrate_output
        '''

        nx, ny = resolution, resolution
        x = np.linspace(-1, 1, nx)
        y = np.linspace(-1, 1, ny)

        xv, yv = np.meshgrid(x, y)

        substrate_input = []
        substrate_hidden = []
        substrate_output = []

        for layer in range(nx):

            # Input
            if not layer:
                substrate_layer = zip(xv[layer], yv[layer])
                substrate_input.append(substrate_layer)
            # Hidden
            elif (layer > 0) and (layer != nx - 1):
                substrate_layer = zip(xv[layer], yv[layer])
                substrate_hidden.append(substrate_layer)

            # Output
            else:
                substrate_layer = zip(xv[layer], yv[layer])
                substrate_output.append(substrate_layer)

        substrate_input, substrate_output = substrate_input[0], substrate_output[0]
        substrate_hidden = list(itertools.chain.from_iterable(substrate_hidden))

        return substrate_input, substrate_hidden, substrate_output
