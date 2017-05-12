########################################################
#   ____  _      ___   _     ____   __    ___   _      #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ |  #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \|  #
#                                                      #
#                  Chad Carlson - 2017                 #
########################################################


import numpy as np
import itertools


__all__ = [ 'NutrientSquare', 'SimpleAgent' ]

class NutrientSquare:

    """
    Simple wrapped callable nutrient environment.

    Todo:
        * Allow for the import of txt file for defining maze/track boundaries.
        * Connect imported boundaries to evaluation loop break collision flag. 
    """

    def __init__(self):

        # -------------------- ENVIRONMENT --------------------

        # Environment parameters

        self.world_size = 100

        self.walls = False
        self.nutrient_rolling_update = False

        # Reward parameters

        self.variable_nutrients = True
        self.nutrient_density = .4

        self.metabolic_cost = -0.25

        self.nutrient_relative_to_cost = 4
        self.nutrient_value = self.nutrient_relative_to_cost * -1 * self.metabolic_cost

        # Build the world

        self.world = self.initialize_environment()

        # -------------------- AGENT --------------------

        # Define Agent object

        self.agent = SimpleAgent(self.world_size)

        # Controller parameters

        self.observation_space = 2 * self.agent.levels_fov ** 2 + self.agent.levels_fov + 1
        self.action_space = 5

        # Possible actions in environment

        self.actions = self.build_actions()

        # -------------------- VISUALIZATION --------------------

        self.agent_relative_to_nutrient = 2
        self.agent_value = self.agent_relative_to_nutrient * self.nutrient_value
        self.agent_world = {0: np.zeros((self.world_size, self.world_size))}

    def build_actions(self):

        """
        Builds an accessible dictionary of possible actions to be called with each agent action to provide adjustments
        for location and heading adjustments. 

        :return: environment action dict. Indices define position and heading adjustments for a selected action.
        """

        # Position adjustments

        empty_position_adjust = [[0, 0], [0, 0], [0, 0], [0, 0]]

        # Position adjustments are different depending on if there is a rolling nutrient update or not

        if self.nutrient_rolling_update:

            # Namely, when the environment 'rolls', the agent can adjust its row, but never its column
            # Is this necessary? couldn't I just have the agent continuously move across the field without
            # changing its heading? If not, then this isn't exactly right, since it would also require the
            # generation of new columns that fit the originally specified nutrient density

            straight = [[-1, 0], [0, 0], [1, 0], [0, 0]]
            diagonal_right = [[-1, 0], [1, 0], [1, 0], [-1, 0]]
            diagonal_left = [[-1, 0], [-1, 0], [1, 0], [1, 0]]

        else:

            straight = [[-1, 0], [0, 1], [1, 0], [0, -1]]
            diagonal_right = [[-1, 1], [1, 1], [1, -1], [-1, -1]]
            diagonal_left = [[-1, -1], [-1, 1], [1, 1], [1, -1]]

        # Build possible actions with position and heading changes

        actions = {
            0: {'heading_adjust': 0, 'position_adjust': straight},
            1: {'heading_adjust': 0, 'position_adjust': diagonal_right},
            2: {'heading_adjust': 0, 'position_adjust': diagonal_left},
            3: {'heading_adjust': -1, 'position_adjust': empty_position_adjust},
            4: {'heading_adjust': 1, 'position_adjust': empty_position_adjust}
        }

        return actions

    def collision_check(self):

        """
        Collision check to potentially break current agent's evaluation.

        :return: collide Boolean 
        """

        collide = False

        if self.walls:

            if self.world[self.agent.location[0], self.agent.location[1]] > self.nutrient_value:
                collide = True

        return collide

    def initialize_environment(self):

        """
        Initialize environment.

        :return: initialized world
        """

        # Define a world with a certain nutrient density

        world = np.random.rand(self.world_size, self.world_size)
        world[world > self.nutrient_density] = 0

        # Inlcude positive rewards

        # Accomodate for variable nutrient values

        if self.variable_nutrients:

            world = self.nutrient_value * (world / self.nutrient_density)  # normalize for density (and maximum values)

        else:

            world[world > 0] = self.nutrient_value

        # Include negative rewards

        world[world == 0] = self.metabolic_cost

        return world

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

        # Re-initialize world

        self.world = self.initialize_environment()

        # Initialize your agent

        init_observation = self.agent.reset(self.world)

        return init_observation

    def return_reward(self):

        """
        Returns reward for agent's current location.

        :return: reward/state at agent.location 
        """

        return self.world[self.agent.location[0], self.agent.location[1]]

    def step(self, action):

        """
        Making a single step through the environment. 

        :return: next observation, current reward, collision Boolean.
        """

        # Agent performs an action that updates agent.location

        decision = self.actions[action]
        self.agent.update(decision)

        # Make  an observation at the current agent.location

        observation = self.agent.observe(self.world)

        # Return the state/reward at the curret agent.location

        state = self.return_reward()

        # Check if a collision flag has been raised for the current agent.location

        collide = self.collision_check()

        # Update the environment in case any nutrients were consumed

        self.update()

        return observation, state, collide

    def update(self):

        """
        Update environment.world with respect possibly consumed nutrients at agent's current location.
        """

        # Agent's current location is updated to reflect current agent.location

        self.world[self.agent.location[0], self.agent.location[1]] = self.metabolic_cost


class SimpleAgent:
    """
    Simple agent object for interacting with Simple Wrapping Environments.
    """

    def __init__(self, world_size):

        # -------------------- REFERENCE --------------------

        self.world_size = world_size

        # -------------------- ORIENTATION --------------------

        # Start the agent in the center of the world
        #   - Note: when walls are placed in, a randomly initialized location
        #       will some times be placed on a pixel where a BREAK will be flagged.
        #       Need to pull from locations where there or not walls OR randomly
        #       choose from selected 'non-walled' positions (i.e. along a starting
        #       point line (and where that line would be at many different locations)

        self.init_location_tag = 'random'
        self.location = self.init_location(self.init_location_tag)

        # Start the agent facing upwards

        self.init_heading_tag = 'random'
        self.heading = self.init_heading(self.init_heading_tag)

        # -------------------- FIELD OF VIEW --------------------

        # Rows in agent FOV

        self.levels_fov = 3

        # Shape of agent FOV

        self.conical_fov = False  # not currently used

    def init_location(self, tag):

        tag_convert = {
            'center': [self.world_size / 2, self.world_size / 2],
            'left': [self.world_size / 2, 0],
            'right': [self.world_size / 2, self.world_size],
            'random': [np.random.randint(self.world_size), np.random.randint(self.world_size)]
        }

        return tag_convert[tag]

    def init_heading(self, tag):

        tag_convert = {'up': 0, 'right': 1, 'down': 2, 'left': 3}
        random_indices = range(len(tag_convert))

        if tag == 'random':

            heading = np.random.randint(len(random_indices))

        else:

            heading = tag_convert[tag]

        return heading

    def cyclical_heading(self, heading):

        """
        Heading conversion. Prevents requests for heading indices that do not exist ( range(4) possible ).

        :param heading: original agent.heading
        :return: converted (cyclical) agent.heading
        """

        if heading < 0:

            heading = 3

        elif heading > 3:

            heading = 0

        return heading

    def enforce_wrapping(self, position):
        """
        Update a world coordinate to ensure that currently inaccessible location can be accessed when called.
        """

        if position >= self.world_size:

            wrapped_position = 0

        elif position < 0:

            wrapped_position = self.world_size - 1

        else:

            wrapped_position = position

        return wrapped_position

    def wrap_agent_location(self):
        """
        Wrapping check main function for an agent's location. 
        """

        if any([self.check_wrapping(coord) for coord in self.location]):
            self.location[0] = self.enforce_wrapping(self.location[0])
            self.location[1] = self.enforce_wrapping(self.location[1])

    def check_wrapping(self, value):
        """
        Checking if a particular coordinate value needs to be wrapped.

        :param value: world coordinate
        :return: bool wrapping decision on world coordinate 
        """

        output = False

        if (value >= self.world_size) or (value < 0):
            output = True

        return output

    def define_fov(self, world):

        """
        Defines the agent's field-of-vision at current location and heading

        :param world: current environment
        :return: observation 
        """

        rows = range(self.location[0] - self.levels_fov, self.location[0] + self.levels_fov + 1)
        cols = range(self.location[1] - self.levels_fov, self.location[1] + self.levels_fov + 1)

        fov = list(itertools.product(rows, cols))

        fov = [(self.enforce_wrapping(i), self.enforce_wrapping(j)) for i, j in fov]

        fov_heading = self.define_fov_heading()

        final_fov = [fov[i] for i in fov_heading]

        # observation = np.array([world[point[0], point[1]] for point in final_fov])  # turn into array. add bias here.

        observation = [world[point[0], point[1]] for point in final_fov]  # turn into array. add bias here.

        # Add a bias

        observation.append(1.0)

        return observation

    def define_fov_heading(self):

        """
        Defines the structure of an agent's field-of-vision

        :return: FOV_heading 
        """

        fov_heading = []

        num_rows = 2 * self.levels_fov + 1
        cells_per_row = self.levels_fov * num_rows
        total_cells_in_full_block = num_rows ** 2

        for level in range(1, self.levels_fov + 1):
            fov_heading += self.heading_row_calc(num_rows, cells_per_row, total_cells_in_full_block, level)

        return fov_heading

    def heading_row_calc(self, r, th, t, l):

        """
        Calculates location indices for individual cells in a row of an agent's field-of-view.

        Todo:
            * Flush out input parameters definitions.
            * Rename input parameters to more readable ones.

        :return output: 
        """

        if not self.heading:

            output = range((self.levels_fov - l) * r, (self.levels_fov - l + 1) * r, 1)

        elif self.heading == 1:

            output = range(r - (self.levels_fov - l + 1), t, r)

        elif self.heading == 2:

            output = range((r - (self.levels_fov - l)) * r - 1, (self.levels_fov + l) * r - 1, -1)

        elif self.heading == 3:

            output = range(2 * th + (self.levels_fov - l), self.levels_fov - l - 1, -1 * r)

        return output

    def reset(self, world):

        """
        Reset agent location and heading in environment to initial values.
        """

        # Restart the agent in the center of the world
        self.location = self.init_location(self.init_location_tag)

        # Restart the agent facing upwards
        self.heading = self.init_heading(self.init_heading_tag)

        init_observation = self.define_fov(world)

        return init_observation

    def observe(self, world):

        return self.define_fov(world)

    def update(self, decision):

        """
        Agent location and heading is updated based on its decision to move.

        :param decision: includes decision['heading_adjust'] and decision['position_adjust']
        :type decision: dict
        """

        # Update heading
        self.heading = self.cyclical_heading(self.heading + decision['heading_adjust'])

        # Update location
        self.location[0] = self.location[0] + decision['position_adjust'][self.heading][0]
        self.location[1] = self.location[1] + decision['position_adjust'][self.heading][1]

        # Wrap updated coordinates if necessary after location update

        self.wrap_agent_location()

class SimpleAgent:
    """
    Simple agent object for interacting with Simple Wrapping Environments.
    """

    def __init__(self, world_size):

        # -------------------- REFERENCE --------------------

        self.world_size = world_size

        # -------------------- ORIENTATION --------------------

        # Start the agent in the center of the world
        #   - Note: when walls are placed in, a randomly initialized location
        #       will some times be placed on a pixel where a BREAK will be flagged.
        #       Need to pull from locations where there or not walls OR randomly
        #       choose from selected 'non-walled' positions (i.e. along a starting
        #       point line (and where that line would be at many different locations)

        self.init_location_tag = 'random'
        self.location = self.init_location(self.init_location_tag)

        # Start the agent facing upwards

        self.init_heading_tag = 'random'
        self.heading = self.init_heading(self.init_heading_tag)

        # -------------------- FIELD OF VIEW --------------------

        # Rows in agent FOV

        self.levels_fov = 3

        # Shape of agent FOV

        self.conical_fov = False  # not currently used

    def init_location(self, tag):

        tag_convert = {
            'center': [self.world_size / 2, self.world_size / 2],
            'left': [self.world_size / 2, 0],
            'right': [self.world_size / 2, self.world_size],
            'random': [np.random.randint(self.world_size), np.random.randint(self.world_size)]
        }

        return tag_convert[tag]

    def init_heading(self, tag):

        tag_convert = {'up': 0, 'right': 1, 'down': 2, 'left': 3}
        random_indices = range(len(tag_convert))

        if tag == 'random':

            heading = np.random.randint(len(random_indices))

        else:

            heading = tag_convert[tag]

        return heading

    def cyclical_heading(self, heading):

        """
        Heading conversion. Prevents requests for heading indices that do not exist ( range(4) possible ).

        :param heading: original agent.heading
        :return: converted (cyclical) agent.heading
        """

        if heading < 0:

            heading = 3

        elif heading > 3:

            heading = 0

        return heading

    def enforce_wrapping(self, position):
        """
        Update a world coordinate to ensure that currently inaccessible location can be accessed when called.
        """

        if position >= self.world_size:

            wrapped_position = 0

        elif position < 0:

            wrapped_position = self.world_size - 1

        else:

            wrapped_position = position

        return wrapped_position

    def wrap_agent_location(self):
        """
        Wrapping check main function for an agent's location. 
        """

        if any([self.check_wrapping(coord) for coord in self.location]):
            self.location[0] = self.enforce_wrapping(self.location[0])
            self.location[1] = self.enforce_wrapping(self.location[1])

    def check_wrapping(self, value):
        """
        Checking if a particular coordinate value needs to be wrapped.

        :param value: world coordinate
        :return: bool wrapping decision on world coordinate 
        """

        output = False

        if (value >= self.world_size) or (value < 0):
            output = True

        return output

    def define_fov(self, world):

        """
        Defines the agent's field-of-vision at current location and heading

        :param world: current environment
        :return: observation 
        """

        rows = range(self.location[0] - self.levels_fov, self.location[0] + self.levels_fov + 1)
        cols = range(self.location[1] - self.levels_fov, self.location[1] + self.levels_fov + 1)

        fov = list(itertools.product(rows, cols))

        fov = [(self.enforce_wrapping(i), self.enforce_wrapping(j)) for i, j in fov]

        fov_heading = self.define_fov_heading()

        final_fov = [fov[i] for i in fov_heading]

        # observation = np.array([world[point[0], point[1]] for point in final_fov])  # turn into array. add bias here.

        observation = [world[point[0], point[1]] for point in final_fov]  # turn into array. add bias here.

        # Add a bias

        observation.append(1.0)

        return observation

    def define_fov_heading(self):

        """
        Defines the structure of an agent's field-of-vision

        :return: FOV_heading 
        """

        fov_heading = []

        num_rows = 2 * self.levels_fov + 1
        cells_per_row = self.levels_fov * num_rows
        total_cells_in_full_block = num_rows ** 2

        for level in range(1, self.levels_fov + 1):
            fov_heading += self.heading_row_calc(num_rows, cells_per_row, total_cells_in_full_block, level)

        return fov_heading

    def heading_row_calc(self, r, th, t, l):

        """
        Calculates location indices for individual cells in a row of an agent's field-of-view.

        Todo:
            * Flush out input parameters definitions.
            * Rename input parameters to more readable ones.

        :return output: 
        """

        if not self.heading:

            output = range((self.levels_fov - l) * r, (self.levels_fov - l + 1) * r, 1)

        elif self.heading == 1:

            output = range(r - (self.levels_fov - l + 1), t, r)

        elif self.heading == 2:

            output = range((r - (self.levels_fov - l)) * r - 1, (self.levels_fov + l) * r - 1, -1)

        elif self.heading == 3:

            output = range(2 * th + (self.levels_fov - l), self.levels_fov - l - 1, -1 * r)

        return output

    def reset(self, world):

        """
        Reset agent location and heading in environment to initial values.
        """

        # Restart the agent in the center of the world
        self.location = self.init_location(self.init_location_tag)

        # Restart the agent facing upwards
        self.heading = self.init_heading(self.init_heading_tag)

        init_observation = self.define_fov(world)

        return init_observation

    def observe(self, world):

        return self.define_fov(world)

    def update(self, decision):

        """
        Agent location and heading is updated based on its decision to move.

        :param decision: includes decision['heading_adjust'] and decision['position_adjust']
        :type decision: dict
        """

        # Update heading
        self.heading = self.cyclical_heading(self.heading + decision['heading_adjust'])

        # Update location
        self.location[0] = self.location[0] + decision['position_adjust'][self.heading][0]
        self.location[1] = self.location[1] + decision['position_adjust'][self.heading][1]

        # Wrap updated coordinates if necessary after location update

        self.wrap_agent_location()

