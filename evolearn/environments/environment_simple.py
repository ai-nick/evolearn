
#######################################################
#   ____  _      ___   _     ____   __    ___   _     #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ | #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \| #
#                                                     #
#                  Chad Carlson - 2017                #
#######################################################


from evolearn.controllers.controller_simple import SimpleAgent

import numpy as np


class SimpleEnvironment:
    """
    Simple wrapped callable nutrient environment.

    Todo:
        * Allow for the import of txt file for defining maze/track boundaries.
    """

    def __init__(self):

        # Environment parameters
        self.world_size = 100
        self.walls = False

        # Reward parameters
        self.variable_nutrients = False
        self.nutrient_density = .25

        self.metabolic_cost = -0.2

        self.nutrient_relative_to_cost = 3
        self.nutrient_value = self.nutrient_relative_to_cost * -1 * self.metabolic_cost

        # Agent parameters
        self.observation_space = 9
        self.action_space = 5

        # Possible actions in environment
        self.actions = self.build_actions()

        # Define Agent object
        self.agent = SimpleAgent()



    def build_actions(self):

        # Position adjustments
        empty_position_adjust = [[0, 0], [0, 0], [0, 0], [0, 0]]
        straight = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        diagonal_right = [[-1, 1], [1, 1], [1, -1], [-1, -1]]
        diagonal_left = [[-1, -1], [-1, 1], [1, 1], [1, -1]]

        actions = {}

        # Position changes
        actions[0] = {'heading_adjust': 0, 'position_adjust': straight}
        actions[1] = {'heading_adjust': 0, 'position_adjust': diagonal_right}
        actions[2] = {'heading_adjust': 0, 'position_adjust': diagonal_left}

        # Heading changes
        actions[3] = {'heading_adjust': -1, 'position_adjust': empty_position_adjust}
        actions[4] = {'heading_adjust': 1, 'position_adjust': empty_position_adjust}

        return actions



    def collision_check(self):

        """
        Collision check to potentially break current agent's evaluation.

        :return: collide Boolean 
        """

        if self.walls:
            if self.world[self.agent.location[0], self.agent.location[1]] > self.nutrient_value:
                collide = True
        else:
            collide = False

        return collide



    def make_observation(self):
        #######################
        """
        Making an observation in a single step through environment.
        """

        pass



    def move_agent(self, action):
        #######################
        """
        Update agent location based on selected action.

        :return: None 
        """



    def reformat_action(self, agent_output):

        """
        Reformat raw network output into environment-specific (or experiment specified) action/class choice.

        :return: reformatted action/class index
        """
        action = agent_output.index(max(agent_output))

        return action




    def reset(self):

        """
        Complete environment reset.

        :return: intial environment observation
        """

        # Define a world with a certain nutrient density
        self.world = np.random.rand(self.world_size, self.world_size)
        self.world[self.world > self.nutrient_density] = 0

        if self.variable_nutrients:
            self.world = self.world / self.nutrient_density  # normalize for density (and maximum values)
        else:
            self.world[self.world > 0] = self.nutrient_value

        self.world[self.world == 0] = self.metabolic_cost

        # Initialize your agent
        self.agent.reset(self.world_size)

        return self.make_observation()




    def return_reward(self):

        """
        Reward return for occupied location.

        :return: reward/state at agent.location 
        """

        return self.world[self.agent.location[0], self.agent.location[1]]




    def step(self, action):

        """
        Making a single step through the environment. 
        """

        self.update(action)

        observation = self.make_observation()

        state = self.return_reward()

        collide = self.collision_check()

        return observation, state, collide




    def update(self, action):

        """
        Update environment.world with respect possibly consumed nutrients at agent's current location.

        :return: None

        """

        self.world[self.agent.location[0], self.agent.location[1]] = self.metabolic_cost





class Recognition:
    """
    General image recognition object.
    """

    def __init__(self):
        pass

