
####################################
# ----------- evolearn ----------- #
####################################

import numpy as np

from evolearn.controllers.controller import SimpleAgent


class SimpleEnvironment:

    """
    Simple wrapped callable nutrient environment.
    
    Todo:
        * Allow for the import of txt file for defining maze/track boundaries.
    """

    def __init__(self):

        # Environment parameters
        self.world_size = 100

        # Reward parameters
        self.variable_nutrients = False
        self.nutrient_density = .25

        self.metabolic_cost = -0.2

        self.nutrient_relative_to_cost = 3
        self.nutrient_value = self.nutrient_relative_to_cost * -1 * self.metabolic_cost

        # Agent parameters
        self.observation_space = 9
        self.action_space = 5

        self.actions = self.build_actions()

        self.agent = SimpleAgent(self.action_space)


    def build_actions(self):

        # Position adjustments
        empty_position_adjust = [ [0,0], [0,0], [0,0], [0,0] ]
        straight = [ [-1,0], [0,1], [1,0], [0,-1] ]
        diagonal_right = [ [-1,1], [1,1], [1,-1], [-1,-1] ]
        diagonal_left = [ [-1,-1], [-1,1], [1,1], [1,-1] ]

        actions = {}

        # Position changes
        actions[0] = { 'heading_adjust': 0, 'position_adjust': straight }
        actions[1] = { 'heading_adjust': 0, 'position_adjust': diagonal_right }
        actions[2] = { 'heading_adjust': 0, 'position_adjust': diagonal_left }

        # Heading changes
        actions[3] = { 'heading_adjust': -1, 'position_adjust': empty_position_adjust }
        actions[4] = { 'heading_adjust': 1, 'position_adjust': empty_position_adjust }

        return actions

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

        # Initialize your agent

        self.agent.reset(self.world)




    def step(self):
        pass
#
#
# env = SimpleEnvironment()
# env.reset()
# print env.agent.location