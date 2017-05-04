
import numpy as np

class WrappingNutrientWorld:

    """Simple wrapped callable nutrient environment.

    :param visualize: (bool) Saves individual frames for visualization. Default False.
        
    """

    def __init__(self, visualize=False):

        self.num_decisions = 500
        self.visualize = visualize

        self.world_size = 100

        # Reward parameters
        self.variable_nutrients = False
        self.nutrient_density = .5
        self.metabolic_cost = -0.2
        self.nutrient_value = 3 * -1 * self.metabolic_cost
        self.world_vals = [ self.metabolic_cost, self.nutrient_value, visualize ]

    def run(self):

        """Runs the environment for specified number of decisions."""

        self.reset()

        for decision in range(self.num_decisions):

            self.step()

    def reset(self):

        """Complete environment reset."""

        # Define a world with a certain nutrient density
        self.world = np.random.rand( self.world_size, self.world_size)
        self.world[self.world > self.nutrient_density] = 0

        if self.variable_nutrients:
            self.world = self.world / self.nutrient_density # normalize for density (and maximum values)
        else:
            self.world[ self.world > 0 ] = self.nutrient_value

        self.world[ self.world == 0 ] = self.metabolic_cost

        # Define an agent
        # self.agent = Agent( self.world, num_decisions, self.world_vals )

    def step(self):

        """Single decision in an environment."""

        # self.agent.step()
        pass


class Recognition:
    def __init__(self):
        pass

