
import numpy as np

class WrappingNutrientWorld:

    """General purpose animation class using matplotlib.

    `WrappingNutrientWorld` creates a wrapped callable nutrient environment.

    # Example

    ```python
        sample = np.random.randn(100, 100, 60)
        anim = Animation(sample)
        anim.animate()
    ```

    # Input shape
        None.

    # Output
        A WrappingNutrientWorld object instance. 

    """

    def __init__(self, visualize=False):

        self.num_decisions = 500
        self.visualize = visualize

        self.world_size = 100

        # Reward parameters
        self.variable_nutrients = True
        self.nutrient_density = .5
        self.metabolic_cost = -0.2
        self.nutrient_value = 3 * -1 * self.metabolic_cost
        self.world_vals = [ self.metabolic_cost, self.nutrient_value, visualize ]

    def run(self):

        self.reset()

        for decision in range(self.num_decisions):

            self.step()

    def reset(self):

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

        # self.agent.step()
        pass


class Recognition:
    def __init__(self):
        pass

