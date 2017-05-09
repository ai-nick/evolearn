
####################################
# ----------- evolearn ----------- #
####################################


import numpy as np


class SimpleEnvironment:

    """
    Simple wrapped callable nutrient environment.
    
    Todo:
        * Allow for the import of txt file for defining maze/track boundaries.
    """

    def __init__(self):

        self.world_size = 100

        # Reward parameters
        self.variable_nutrients = False
        self.nutrient_density = .5
        self.metabolic_cost = -0.2
        self.nutrient_value = 3 * -1 * self.metabolic_cost


    def reset(self):

        """
        Complete environment reset.
        """

        # Define a world with a certain nutrient density
        self.world = np.random.rand( self.world_size, self.world_size)
        self.world[self.world > self.nutrient_density] = 0

        if self.variable_nutrients:
            self.world = self.world / self.nutrient_density # normalize for density (and maximum values)
        else:
            self.world[ self.world > 0 ] = self.nutrient_value

        self.world[ self.world == 0 ] = self.metabolic_cost


    def step(self):
        pass
