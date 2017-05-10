
####################################
# ----------- evolearn ----------- #
####################################


class SimpleAgent:

    """
    Simple agent object for interacting with Simple Wrapping Environments.
    """

    def __init__(self, action_space):

        # Observation parameters
        self.levels_FOV = 1
        self.conical_FOV = False

        # Action parameters
        self.action_space = action_space


    def reset(self, world_size):

        # Reset dynamic parameters changed by actions

        # Start off the agent in the center of the world
        self.location = [ world_size/2, world_size/2 ]

        # Start off the agent facing upwards
        self.heading = 0

