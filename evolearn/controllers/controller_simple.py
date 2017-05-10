
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

    def __init__(self):

        # Observation parameters - currently not used
        self.levels_FOV = 1
        self.conical_FOV = False




    def cyclical_heading(self, heading):

        """
        Heading conversion. Prevents requests for heading indices that do not exist ( range(4) possible ).

        :param heading: original agent.heading
        :return heading: converted (cyclical) agent.heading
        """

        if heading < 0:
            heading = 3
        elif heading > 3:
            heading = 0

        return heading




    def define_FOV(self):

        """
        
        :return observation: 
        """

        rows = range(self.location[0] - (self.levels_FOV), self.location[0] + (self.levels_FOV + 1))
        cols = range(self.location[1] - (self.levels_FOV), self.location[1] + (self.levels_FOV + 1))

        FOV = list(itertools.product(rows, cols))
        FOV = [(self.enforce_wrapping(i), self.enforce_wrapping(j)) for i, j in FOV]

        FOV_heading = self.define_FOV_heading()

        final_FOV = [FOV[i] for i in FOV_heading]

        observation = np.array([self.world[point[0], point[1]] for point in final_FOV])

        return observation




    def define_FOV_heading(self):

        """

        :return FOV_heading: 
        """

        FOV_heading = []
        r = 2 * self.levels_FOV + 1
        tH = self.levels_FOV * r
        t = r ** 2

        for l in range(1, self.levels_FOV + 1):

            FOV_heading += self.heading_row_calc(r, tH, t, l)

        return FOV_heading




    def enforce_wrapping(self, position):

        """
        Location conversion. Prevents requests for locations that are not pre-allocated.

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





    def heading_row_calc(self, r, tH, t, l):

        """

        :return output: 
        """

        if not self.heading:

            output = range((self.levels_FOV - l) * r, (self.levels_FOV - l + 1) * r, 1)

        elif self.heading == 1:

            output = range(r - (self.levels_FOV - l + 1), t, r)

        elif self.heading == 2:

            output = range((r - (self.levels_FOV - l)) * r - 1, (self.levels_FOV + l) * r - 1, -1)

        elif self.heading == 3:

            output = range(2 * tH + (self.levels_FOV - l), self.levels_FOV - l - 1, -1 * r)

        return output




    def reset(self, world_size):

        """
        Agent Object reset location and heading in environment.

        :param world_size: environment dimensions (square).
        :return: 
        """

        # Save env.world_size globally
        self.world_size = world_size

        # Restart the agent in the center of the world
        self.location = [self.world_size / 2, self.world_size / 2]

        # Restart the agent facing upwards
        self.heading = 0



