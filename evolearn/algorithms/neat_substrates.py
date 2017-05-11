

class Substrate:

    """
    Substrate class for sampling potential phenotype node locations.
    """

    def __init__(self, type):

        self.type = type
        self.substrate = self.define_substrate()

    def define_substrate(self):

        substrate = 'unknown'

        if self.type == 'simple':

            substrate = [ [(-1, -1), (-1, 0), (-1, 1)], [(0, -1), (0, 0), (0, 1)], [(1, 0)] ]

        elif self.type == '5x5':
            pass

        elif self.type == '10x10':
            pass

        elif self.type == '25x25':
            pass

        elif self.type == '100x100':
            pass

        elif self.type == 'ES':
            pass

        return substrate
#
# sub = Substrate('simple')
# print sub.substrate[0]