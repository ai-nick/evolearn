
########################################################
#   ____  _      ___   _     ____   __    ___   _      #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ |  #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \|  #
#                                                      #
#                  Chad Carlson - 2017                 #
########################################################


import itertools
import numpy as np


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

        tag_convert = { 'up': 0, 'right': 1, 'down': 2, 'left': 3 }
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
        r = 2 * self.levels_fov + 1
        th = self.levels_fov * r
        t = r ** 2

        for l in range(1, self.levels_fov + 1):

            fov_heading += self.heading_row_calc(r, th, t, l)

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
        self.heading = self.cyclical_heading( self.heading + decision['heading_adjust'] )

        # Update location
        self.location[0] = self.location[0] + decision['position_adjust'][self.heading][0]
        self.location[1] = self.location[1] + decision['position_adjust'][self.heading][1]

        # Wrap updated coordinates if necessary after location update

        self.wrap_agent_location()

