
#######################################################
#   ____  _      ___   _     ____   __    ___   _     #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ | #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \| #
#                                                     #
#                  Chad Carlson - 2017                #
#######################################################


class SimpleAgent:

    """
    Simple agent object for interacting with Simple Wrapping Environments.
    """

    def __init__(self):

        # Observation parameters - currently not used
        self.levels_FOV = 1
        self.conical_FOV = False

    def reset(self, world_size):

        # Reset dynamic parameters changed by actions

        # Start off the agent in the center of the world
        self.location = [ world_size/2, world_size/2 ]

        # Start off the agent facing upwards
        self.heading = 0

