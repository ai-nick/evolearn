
#######################################################
#   ____  _      ___   _     ____   __    ___   _     #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ | #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \| #
#                                                     #
#                  Chad Carlson - 2017                #
#######################################################


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

        self.location = [self.world_size / 2, self.world_size / 2]

        # Start the agent facing upwards

        self.heading = 0

        # -------------------- FIELD OF VIEW --------------------

        # Rows in agent FOV

        self.levels_fov = 1

        # Shape of agent FOV

        self.conical_fov = False  # not currently used

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

    def define_fov(self, world):

        """
        Defines the agent's field-of-vision.
        
        :param world: current environment
        :return: observation 
        """

        rows = range(self.location[0] - self.levels_fov, self.location[0] + self.levels_fov + 1)
        cols = range(self.location[1] - self.levels_fov, self.location[1] + self.levels_fov + 1)

        fov = list(itertools.product(rows, cols))
        fov = [(self.enforce_wrapping(i), self.enforce_wrapping(j)) for i, j in fov]

        fov_heading = self.define_fov_heading()

        final_fov = [fov[i] for i in fov_heading]

        observation = np.array([world[point[0], point[1]] for point in final_fov])

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

    def enforce_wrapping(self, position):

        """
        Location conversion. Prevents requests for locations that are not accessible in the current environment.

        :param position: world positionX or world positionY
        :return: new world positionX or world positionY

        """

        if position >= self.world_size:

            wrapped_position = 0

        elif position < 0:

            wrapped_position = self.world_size - 1

        else:

            wrapped_position = position

        return wrapped_position

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

    def reset(self):

        """
        Reset agent location and heading in environment to initial values.
        """

        # Restart the agent in the center of the world
        self.location = [self.world_size / 2, self.world_size / 2]

        # Restart the agent facing upwards
        self.heading = 0
